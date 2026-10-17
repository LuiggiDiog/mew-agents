# E2E playbook (Playwright)

How to design, write, stabilize, and maintain end-to-end tests in this repository. `AGENTS.md` holds the binding rules; setup and commands are in `docs/testing.md`.

## 1. Core principles

1. Test user-visible behavior, not implementation details.
2. Use the smallest reliable scope: one spec or one test before any wider run.
3. Use deterministic waits (auto-retrying `expect`, `waitForURL`, explicit state checks). Never synchronize with `waitForTimeout`.
4. Real app behavior first. Mock only external, non-deterministic boundaries, and only for a concrete reason.
5. Keep specs, page objects, and flow documentation in sync.

## 2. Before writing a spec

Write down:

- **Flow map:** route sequence, required user actions, validation rules, and expected destination URLs.
- **State progression:** which actions create state that later steps depend on.
- **External dependencies:** third-party APIs or providers and how they are faked in the test environment.
- **Environment contract:** base URL, required env vars, feature flags.
- **Data constraints:** fields that must be unique.

## 3. Structure

```txt
{{E2E_DIR}}/
  fixtures/
    test-data.ts        # static non-unique values + runtime unique generators
  helpers/
    *.ts                # shared anti-flake utilities and setup factories
  pages/
    *.page.ts           # one page object per page, each with assertLoaded()
  *.spec.ts             # one spec per user flow
{{E2E_CONFIG}}
```

- One page object per page or domain area. It exposes stable actions and an `assertLoaded()` that checks the URL and a landmark element.
- Extract a config detail or setup step into `helpers/` once it repeats in three or more specs.
- Keep specs readable as a user story: arrange via page objects, act, assert.

Page object pattern:

```ts
import { expect, type Page } from '@playwright/test';

export class HomePage {
  constructor(private readonly page: Page) {}

  async goto() {
    await this.page.goto('/');
    await this.assertLoaded();
  }

  async assertLoaded() {
    await expect(this.page).toHaveURL('/');
    await expect(this.page.getByRole('main')).toBeVisible();
  }
}
```

## 4. Real vs mock, per step

| Question                                                         | If yes                                            | If no            |
| ---------------------------------------------------------------- | ------------------------------------------------- | ---------------- |
| Does this step create state used by later steps?                 | Use the real UI/API                               | Mock is possible |
| Does the server decide the next route from this response?        | Use the real response or a tightly scoped fake    | No mock needed   |
| Is it a third-party provider outside the product?                | Keep the app flow real; fake only that boundary   | Standard flow    |
| Could the mock break session or cache assumptions?               | Do not mock it                                    | Mock can work    |

{{STACK:e2e-gotchas}}

## 5. Spec design

- **Isolated tests by default.** They are more reliable and can run in parallel. Use `storageState` or API bootstrap to skip expensive repeated setup.
- **Serial only for true journeys.** Use `test.describe.serial` only when each step depends on the previous step's session or state.
- **No bridge-only tests.** Do not add a test that only asserts a transient redirect when the next functional test already validates it; fold the assertion into that test's preamble.
- **Assert exact destinations:** `await expect(page).toHaveURL('/exact/path')`.
- **Tag by module.** Tag each spec with the feature folder it covers, so a change in that folder selects its specs with `--grep "@<module>"`. A spec that crosses modules carries each tag.

```ts
test.describe('checkout', { tag: '@checkout' }, () => {
  test('pays with a saved card', async ({ page }) => {
    // ...
  });
});
```

## 6. Locators (priority order)

1. `getByRole` with accessible name
2. `getByLabel`
3. `getByTestId`
4. Scoped CSS, as a last resort

- Prefer stable contracts: roles, labels, explicit `data-testid`.
- Scope to a container (`page.getByRole('dialog').getByRole('button', { name: 'Guardar' })`) to avoid strict-mode multiple matches.
- A missing accessible name in a locator is usually an accessibility bug in the UI; fix the UI rather than falling back to CSS.

## 7. Anti-flake patterns

- **Readiness, not presence.** Before acting on computed screens, check the expected value is visible and the CTA is enabled: `await expect(button).toBeEnabled()`.
- **Overlays.** Toasts and portals can intercept clicks. Wait for them to disappear (`await expect(toast).toBeHidden()`) before critical clicks. Use a forced or DOM click helper only when the overlay is outside the behavior under test, and keep it in `helpers/`.
- **Navigation.** Pair the action with the wait: `await Promise.all([page.waitForURL('/next'), button.click()])`, or click then `await expect(page).toHaveURL('/next')`.

## 8. Unique data and bounded retries

Generate unique values at runtime (timestamp or random suffix). Retry only known recoverable conflicts, such as a duplicate unique field:

```ts
for (let attempt = 1; attempt <= 3; attempt++) {
  await form.submit();

  const succeeded = await page
    .waitForURL('/expected-destination', { timeout: 20_000 })
    .then(() => true)
    .catch(() => false);
  if (succeeded) break;

  if (attempt < 3 && (await form.isDuplicateErrorVisible())) {
    await form.fillUniqueField(uniqueValue());
    continue;
  }

  throw new Error(`Submission failed at ${page.url()}`);
}
```

- Keep attempts bounded (3–5).
- Fail with the current URL and the reason.

## 9. Asserting error states

Synthetic invalid input (a malformed token, garbage payload) is usually rejected at a parsing or auth layer, so the UI never reaches the branch for the specific business error. Walk the real path that produces the state instead:

- "Already used" → use it successfully, then reuse it.
- "Session expired or revoked" → sign out through the UI, then retry.
- "Invalid state" → complete the step that invalidates it.

Prefer UI sign-out over clearing storage or cookies directly; it exercises the real flow.

## 10. Timeouts

| Step type                         | Test timeout |
| --------------------------------- | ------------ |
| Basic page or form                | 30–60 s      |
| Upload + server processing        | 60–180 s     |
| External provider round trip      | 2–5 min      |

Raise a timeout only after confirming the flow is functionally correct. A timeout reflects expected latency; it must not hide broken logic.

## 11. Optional: video evidence

Off by default. When a run is meant to be shared with non-engineers:

- Record at viewport size (`video: { mode: 'on', size: { width: 1280, height: 720 } }`); the default 800×450 is blurry. Contexts created with `browser.newContext()` need `recordVideo.size` set explicitly, so use a factory in `helpers/`.
- Gate demo pauses behind an env var (`E2E_DEMO_PAUSES=true`) so normal runs stay fast.

## 12. Mobile checks

Mobile specs are named `<flow>.mobile.spec.ts` and run in their own project, so desktop specs do not run twice. Add the project to `{{E2E_CONFIG}}` with the first mobile spec:

```ts
projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] }, testIgnore: /\.mobile\.spec\.ts$/ },
  // Chromium-based device: mobile viewport and touch without installing WebKit.
  { name: 'mobile', use: { ...devices['Pixel 7'] }, testMatch: /\.mobile\.spec\.ts$/ },
],
```

Run one with the `e2e` command and `--project=mobile <spec>`. Emulation covers viewport, touch, and user agent, not iOS Safari rendering; say so when reporting (`devices['iPhone 13']` needs the WebKit browser).

`{{E2E_DIR}}/helpers/mobile.ts`, created with the first mobile spec:

```ts
import { expect, type Locator, type Page } from '@playwright/test';

/** Fails when the page scrolls horizontally, naming the elements that stick out. */
export async function expectNoHorizontalOverflow(page: Page) {
  const { overflow, offenders } = await page.evaluate(() => {
    const root = document.documentElement;
    const overflow = root.scrollWidth - root.clientWidth;
    const offenders =
      overflow > 0
        ? [...document.body.querySelectorAll<HTMLElement>('*')]
            .filter((el) => el.getBoundingClientRect().right > root.clientWidth + 1)
            .slice(0, 5)
            .map((el) => el.outerHTML.slice(0, 120))
        : [];
    return { overflow, offenders };
  });
  expect(overflow, `page scrolls horizontally:\n${offenders.join('\n')}`).toBeLessThanOrEqual(0);
}

/** Fails when a visible control inside `scope` is under `min` CSS pixels (WCAG 2.5.8). */
export async function expectTouchTargets(scope: Locator, min = 24) {
  const small = await scope.evaluate((root, min) => {
    const controls =
      'a[href], button, input:not([type="hidden"]), select, textarea, summary, [role="button"], [role="link"], [role="tab"], [role="checkbox"], [role="switch"]';
    return [...root.querySelectorAll<HTMLElement>(controls)]
      // Inline text links are exempt; a labeled input's label is part of its target.
      .filter((el) => getComputedStyle(el).display !== 'inline')
      .filter((el) => !(el instanceof HTMLInputElement && el.labels?.length))
      // Visually hidden elements (sr-only, visually-hidden) are not targets.
      .filter((el) => {
        const style = getComputedStyle(el);
        return !style.clip.startsWith('rect') && !style.clipPath.startsWith('inset(50%');
      })
      .map((el) => ({ el, box: el.getBoundingClientRect() }))
      .filter(({ box }) => box.width > 1 && box.height > 1 && (box.width < min || box.height < min))
      .map(({ el, box }) => `${Math.round(box.width)}x${Math.round(box.height)} ${el.outerHTML.slice(0, 80)}`);
  }, min);
  expect(small, `controls smaller than ${min}px`).toEqual([]);
}
```

A mobile spec checks each agreed width after the page is ready:

```ts
import { test } from '@playwright/test';
import { expectNoHorizontalOverflow, expectTouchTargets } from './helpers/mobile';
import { CheckoutPage } from './pages/checkout.page';

for (const width of [320, 375]) {
  test(`checkout fits a ${width}px screen`, async ({ page }) => {
    await page.setViewportSize({ width, height: 800 });
    await new CheckoutPage(page).goto();
    await expectNoHorizontalOverflow(page);
    await expectTouchTargets(page.getByRole('main'));
  });
}
```

## 13. Validation order

Follow the test selection ladder in `AGENTS.md` (Validation). For E2E it means:

1. `e2e --list` after structural edits.
2. While iterating: the changed spec with `--grep "<title>"` and `-x`, against the dev server.
3. Before reporting, once: `e2e-prod` with the union of spec files from `e2e --list --only-changed` and from `grep -rl "@<module>"` for each touched module, passed as explicit paths (both filters in one command intersect). Use `--only-changed=<base>` when the work is committed; if a touched module has no tagged spec, find its specs by route, page object, or visible text. An empty selection is never green.
4. After fixing failures: the command that failed, with `--last-failed`.
5. The complete suite only when the user asks for it.

On failure: open the trace first, then capture the URL, visible blockers, and console errors. Document the root cause and fix pattern.

## 14. Failure signatures

| Symptom                                   | Typical cause                                 | Fix                                                 |
| ----------------------------------------- | --------------------------------------------- | --------------------------------------------------- |
| Click timeout, pointer intercepted        | Toast or portal overlay                       | Wait for overlay hidden; scoped click helper        |
| Strict-mode violation                     | Locator matches several elements              | Scope to a container or use the accessible name     |
| Retry treated as success on wrong page    | Weak success condition                        | Assert the exact destination URL                    |
| Flaky redirect assertion                  | Separate bridge-only test                     | Fold into the next functional test                  |
| Expected business error never appears     | Input rejected at a parsing or auth layer     | Walk the real path that produces the state          |
| Process hangs after a failed run          | HTML reporter opened a server                 | `reporter: [['html', { open: 'never' }]]`           |
| Passes locally, fails on a clean run      | Reused dev server or leftover data            | `reuseExistingServer: false`; unique runtime data   |
| Every spec runs twice                     | Mobile project without `testMatch`            | Split projects by the `.mobile.spec.ts` suffix      |
| Overflow check passes, page still clipped | `overflow-x: hidden` on `html` or `body`      | Remove it and fix the element that sticks out       |

## 15. Spec checklist

- [ ] Flow map and destination URLs written down.
- [ ] Real vs mock decided per step; server-side fakes go through env.
- [ ] One page object per page with `assertLoaded()`.
- [ ] Role/label locators; no raw CSS without a reason.
- [ ] No `waitForTimeout` for synchronization.
- [ ] Unique runtime data; bounded retries only for known conflicts.
- [ ] Exact URL assertions; no bridge-only tests.
- [ ] Flows with a mobile concern have a `*.mobile.spec.ts` with overflow and target checks at the agreed widths.
- [ ] Tagged with the module it covers (`@<module>`).
- [ ] Validated with `--list`, then the ladder: targeted spec on the dev server, final run with `e2e-prod`.
- [ ] Flow docs updated in the same change.
