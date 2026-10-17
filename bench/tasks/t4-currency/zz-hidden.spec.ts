import { expect, test } from '@playwright/test';

test('hidden: catalog and cart show soles', async ({ page }) => {
  await page.goto('/');
  const coffee = page.getByRole('region', { name: 'Products' }).getByRole('listitem').filter({ hasText: 'Coffee' });
  await expect(coffee).toContainText('S/ 3.00');
  await coffee.getByRole('button').click();
  await expect(page.getByRole('region', { name: 'Cart' }).getByText('Total: S/ 3.00')).toBeVisible();
  await expect(page.getByText(/\$/)).toHaveCount(0);
});
