import { expect, type Page } from '@playwright/test';

export class ShopPage {
  constructor(private readonly page: Page) {}

  async goto() {
    await this.page.goto('/');
    await this.assertLoaded();
  }

  async assertLoaded() {
    await expect(this.page).toHaveURL('/');
    await expect(this.page.getByRole('heading', { name: 'Bench Shop' })).toBeVisible();
  }

  products() {
    return this.page.getByRole('region', { name: 'Products' });
  }

  product(productName: string) {
    return this.products().getByRole('listitem').filter({ hasText: productName });
  }

  async addToCart(productName: string) {
    await this.product(productName).getByRole('button', { name: 'Add to crat' }).click();
  }

  cart() {
    return this.page.getByRole('region', { name: 'Cart' });
  }
}
