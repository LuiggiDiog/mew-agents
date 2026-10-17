import { expect, test } from '@playwright/test';
import { ShopPage } from './pages/shop.page';

const products = [
  ['Coffee', '$3.00'],
  ['Tea', '$2.50'],
  ['Cake', '$4.25'],
] as const;

test.describe('cart', { tag: '@cart' }, () => {
  for (const [name, price] of products) {
    test(`adds ${name} and shows the total`, async ({ page }) => {
      const shop = new ShopPage(page);
      await shop.goto();
      await shop.addToCart(name);
      await expect(shop.cart().getByText(`${name} × 1 — ${price}`)).toBeVisible();
      await expect(shop.cart().getByText(`Total: ${price}`)).toBeVisible();
    });
  }

  test('groups repeated products in one row', async ({ page }) => {
    const shop = new ShopPage(page);
    await shop.goto();
    await shop.addToCart('Coffee');
    await shop.addToCart('Coffee');
    await expect(shop.cart().getByText('Coffee × 2 — $6.00')).toBeVisible();
  });

  test('sums different products', async ({ page }) => {
    const shop = new ShopPage(page);
    await shop.goto();
    await shop.addToCart('Coffee');
    await shop.addToCart('Tea');
    await expect(shop.cart().getByText('Total: $5.50')).toBeVisible();
  });
});
