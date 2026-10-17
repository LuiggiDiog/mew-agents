import CartPanel from './modules/cart/components/CartPanel';
import { useCart } from './modules/cart/hooks/useCart';
import ProductList from './modules/catalog/components/ProductList';
import { products } from './modules/catalog/data/products';

export default function App() {
  const { cart, add } = useCart();

  return (
    <>
      <header>
        <h1>Bench Shop</h1>
      </header>
      <main>
        <ProductList products={products} onAdd={add} />
        <CartPanel cart={cart} />
      </main>
    </>
  );
}
