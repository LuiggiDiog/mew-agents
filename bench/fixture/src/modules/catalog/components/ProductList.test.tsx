import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { products } from '../data/products';
import ProductList from './ProductList';

describe('ProductList', () => {
  it('lists every product', () => {
    render(<ProductList products={products} onAdd={() => {}} />);
    expect(screen.getAllByRole('listitem')).toHaveLength(3);
  });

  it('shows each price', () => {
    render(<ProductList products={products} onAdd={() => {}} />);
    expect(screen.getByText('$3.00')).toBeInTheDocument();
    expect(screen.getByText('$4.25')).toBeInTheDocument();
  });

  it('adds the chosen product', async () => {
    const onAdd = vi.fn();
    render(<ProductList products={products} onAdd={onAdd} />);
    await userEvent.click(screen.getAllByRole('button', { name: 'Add to crat' })[1]);
    expect(onAdd).toHaveBeenCalledWith(products[1]);
  });
});
