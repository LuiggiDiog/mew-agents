import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { products } from '../../catalog/data/products';
import { addItem, emptyCart } from '../services/cart';
import CartPanel from './CartPanel';

describe('CartPanel', () => {
  it('shows the empty state', () => {
    render(<CartPanel cart={emptyCart} />);
    expect(screen.getByText('Your cart is empty')).toBeInTheDocument();
  });

  it('shows each item and the total', () => {
    render(<CartPanel cart={addItem(emptyCart, products[0])} />);
    expect(screen.getByText('Coffee × 1 — $3.00')).toBeInTheDocument();
    expect(screen.getByText('Total: $3.00')).toBeInTheDocument();
  });
});
