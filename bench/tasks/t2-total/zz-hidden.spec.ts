import { expect, test } from '@playwright/test';

test('hidden: total counts every unit', async ({ page }) => {
  await page.goto('/');
  const addCoffee = page
    .getByRole('region', { name: 'Products' })
    .getByRole('listitem')
    .filter({ hasText: 'Coffee' })
    .getByRole('button');
  await addCoffee.click();
  await addCoffee.click();
  await expect(page.getByRole('region', { name: 'Cart' }).getByText('Total: $6.00')).toBeVisible();
});
