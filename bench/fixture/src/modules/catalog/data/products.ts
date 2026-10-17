export type ProductT = {
  id: string;
  name: string;
  price: number;
};

export const products: ProductT[] = [
  { id: 'coffee', name: 'Coffee', price: 3 },
  { id: 'tea', name: 'Tea', price: 2.5 },
  { id: 'cake', name: 'Cake', price: 4.25 },
];
