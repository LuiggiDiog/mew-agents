import { expect, test } from '@playwright/test';
import { ShopPage } from './pages/shop.page';

test.describe('empty cart', { tag: '@cart' }, () => {
  test('starts empty', async ({ page }) => {
    const shop = new ShopPage(page);
    await shop.goto();
    await expect(shop.cart().getByText('Your cart is empty')).toBeVisible();
  });

  test('hides the total while empty', async ({ page }) => {
    const shop = new ShopPage(page);
    await shop.goto();
    await expect(shop.cart().getByText(/Total:/)).toHaveCount(0);
  });

  for (const name of ['Coffee', 'Tea', 'Cake']) {
    test(`leaves the empty state after adding ${name}`, async ({ page }) => {
      const shop = new ShopPage(page);
      await shop.goto();
      await shop.addToCart(name);
      await expect(shop.cart().getByText('Your cart is empty')).toHaveCount(0);
    });
  }
});
