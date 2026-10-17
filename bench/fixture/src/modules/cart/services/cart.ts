import type { ProductT } from '../../catalog/data/products';

export type CartItemT = {
  productId: string;
  name: string;
  price: number;
  quantity: number;
};

export type CartT = {
  items: CartItemT[];
};

export const emptyCart: CartT = { items: [] };

export function addItem(cart: CartT, product: ProductT): CartT {
  const existing = cart.items.find((item) => item.productId === product.id);
  if (existing) {
    return {
      items: cart.items.map((item) =>
        item.productId === product.id ? { ...item, quantity: item.quantity + 1 } : item,
      ),
    };
  }
  return {
    items: [...cart.items, { productId: product.id, name: product.name, price: product.price, quantity: 1 }],
  };
}

export function total(cart: CartT): number {
  return cart.items.reduce((sum, item) => sum + item.price, 0);
}

export function formatPrice(value: number): string {
  return `$${value.toFixed(2)}`;
}
