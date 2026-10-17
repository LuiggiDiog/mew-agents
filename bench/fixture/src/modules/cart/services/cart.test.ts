import { describe, expect, it } from 'vitest';
import { products } from '../../catalog/data/products';
import { addItem, emptyCart, formatPrice, total } from './cart';

const [coffee, tea] = products;

describe('cart', () => {
  it('adds a new product as one item', () => {
    const cart = addItem(emptyCart, coffee);
    expect(cart.items).toEqual([{ productId: 'coffee', name: 'Coffee', price: 3, quantity: 1 }]);
  });

  it('increments the quantity of a product already in the cart', () => {
    const cart = addItem(addItem(emptyCart, coffee), coffee);
    expect(cart.items).toHaveLength(1);
    expect(cart.items[0].quantity).toBe(2);
  });

  it('sums the price of different products', () => {
    expect(total(addItem(addItem(emptyCart, coffee), tea))).toBe(5.5);
  });

  it('formats prices with two decimals', () => {
    expect(formatPrice(4.25)).toBe('$4.25');
  });
});
