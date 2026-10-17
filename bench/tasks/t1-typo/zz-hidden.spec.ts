import { expect, test } from '@playwright/test';

test('hidden: product buttons read "Add to cart"', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'Add to cart' })).toHaveCount(3);
  await expect(page.getByText(/crat/i)).toHaveCount(0);
});
