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

## 12. Validation order

1. `{{CMD_E2E}} --list` after structural edits.
2. The changed spec or test (`--grep "<title>"`).
3. The full flow or suite only when coupling risk exists and the user asked for it.

On failure: open the trace first, then capture the URL, visible blockers, and console errors. Document the root cause and fix pattern.

## 13. Failure signatures

| Symptom                                   | Typical cause                                 | Fix                                                 |
| ----------------------------------------- | --------------------------------------------- | --------------------------------------------------- |
| Click timeout, pointer intercepted        | Toast or portal overlay                       | Wait for overlay hidden; scoped click helper        |
| Strict-mode violation                     | Locator matches several elements              | Scope to a container or use the accessible name     |
| Retry treated as success on wrong page    | Weak success condition                        | Assert the exact destination URL                    |
| Flaky redirect assertion                  | Separate bridge-only test                     | Fold into the next functional test                  |
| Expected business error never appears     | Input rejected at a parsing or auth layer     | Walk the real path that produces the state          |
| Process hangs after a failed run          | HTML reporter opened a server                 | `reporter: [['html', { open: 'never' }]]`           |
| Passes locally, fails on a clean run      | Reused dev server or leftover data            | `reuseExistingServer: false`; unique runtime data   |

## 14. Spec checklist

- [ ] Flow map and destination URLs written down.
- [ ] Real vs mock decided per step; server-side fakes go through env.
- [ ] One page object per page with `assertLoaded()`.
- [ ] Role/label locators; no raw CSS without a reason.
- [ ] No `waitForTimeout` for synchronization.
- [ ] Unique runtime data; bounded retries only for known conflicts.
- [ ] Exact URL assertions; no bridge-only tests.
- [ ] Validated with `--list`, then the targeted spec.
- [ ] Flow docs updated in the same change.
