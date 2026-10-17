import { useState } from 'react';
import type { ProductT } from '../../catalog/data/products';
import { addItem, emptyCart, type CartT } from '../services/cart';

export function useCart() {
  const [cart, setCart] = useState<CartT>(emptyCart);

  const add = (product: ProductT) => setCart((current) => addItem(current, product));

  return { cart, add };
}
