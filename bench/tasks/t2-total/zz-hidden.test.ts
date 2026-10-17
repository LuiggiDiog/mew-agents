import { describe, expect, it } from 'vitest';
import { products } from '../../catalog/data/products';
import { addItem, emptyCart, total } from './cart';

const [coffee, tea, cake] = products;

describe('hidden: total', () => {
  it('multiplies each price by its quantity', () => {
    expect(total(addItem(addItem(emptyCart, coffee), coffee))).toBe(6);
  });

  it('mixes products and quantities', () => {
    let cart = addItem(emptyCart, coffee);
    cart = addItem(cart, coffee);
    cart = addItem(cart, tea);
    cart = addItem(cart, cake);
    expect(total(cart)).toBe(12.75);
  });

  it('is zero for an empty cart', () => {
    expect(total(emptyCart)).toBe(0);
  });
});
