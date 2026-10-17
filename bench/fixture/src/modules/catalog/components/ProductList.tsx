import { formatPrice } from '../../cart/services/cart';
import type { ProductT } from '../data/products';

type PropsT = {
  products: ProductT[];
  onAdd: (product: ProductT) => void;
};

export default function ProductList(props: PropsT) {
  const { products, onAdd } = props;

  return (
    <section aria-labelledby="products-title">
      <h2 id="products-title">Products</h2>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <span>{product.name}</span> <span>{formatPrice(product.price)}</span>{' '}
            <button type="button" onClick={() => onAdd(product)}>
              Add to crat
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
