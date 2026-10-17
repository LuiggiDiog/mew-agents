import { expect, test } from '@playwright/test';
import { ShopPage } from './pages/shop.page';

const prices = [
  ['Coffee', '$3.00'],
  ['Tea', '$2.50'],
  ['Cake', '$4.25'],
] as const;

test.describe('catalog', { tag: '@catalog' }, () => {
  test('lists every product', async ({ page }) => {
    await new ShopPage(page).goto();
    await expect(new ShopPage(page).products().getByRole('listitem')).toHaveCount(3);
  });

  for (const [name, price] of prices) {
    test(`shows the price of ${name}`, async ({ page }) => {
      const shop = new ShopPage(page);
      await shop.goto();
      await expect(shop.product(name)).toContainText(price);
    });
  }
});
