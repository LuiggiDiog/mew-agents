import { expect, test } from '@playwright/test';
import { ShopPage } from './pages/shop.page';

test.describe('catalog accessibility', { tag: '@catalog' }, () => {
  test('has a page heading and a products heading', async ({ page }) => {
    await new ShopPage(page).goto();
    await expect(page.getByRole('heading', { level: 1, name: 'Bench Shop' })).toBeVisible();
    await expect(page.getByRole('heading', { level: 2, name: 'Products' })).toBeVisible();
  });

  for (const name of ['Coffee', 'Tea', 'Cake']) {
    test(`${name} has a reachable add button`, async ({ page }) => {
      const shop = new ShopPage(page);
      await shop.goto();
      const button = shop.product(name).getByRole('button');
      await button.focus();
      await expect(button).toBeFocused();
    });
  }
});
