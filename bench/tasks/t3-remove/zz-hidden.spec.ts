import { expect, test } from '@playwright/test';

test('hidden: remove takes one unit at a time', async ({ page }) => {
  await page.goto('/');
  const add = (name: string) =>
    page.getByRole('region', { name: 'Products' }).getByRole('listitem').filter({ hasText: name }).getByRole('button').click();
  const cart = page.getByRole('region', { name: 'Cart' });

  await add('Coffee');
  await add('Coffee');
  await add('Tea');
  await cart.getByRole('button', { name: 'Remove Coffee' }).click();
  await expect(cart.getByText(/Coffee × 1/)).toBeVisible();

  await cart.getByRole('button', { name: 'Remove Coffee' }).click();
  await expect(cart.getByText(/Coffee/)).toHaveCount(0);
  await expect(cart.getByText(/Tea × 1/)).toBeVisible();

  await cart.getByRole('button', { name: 'Remove Tea' }).click();
  await expect(cart.getByText('Your cart is empty')).toBeVisible();
});
