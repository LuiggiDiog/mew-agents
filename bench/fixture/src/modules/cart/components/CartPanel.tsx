import { formatPrice, total, type CartT } from '../services/cart';

type PropsT = {
  cart: CartT;
};

export default function CartPanel(props: PropsT) {
  const { cart } = props;

  return (
    <section aria-labelledby="cart-title">
      <h2 id="cart-title">Cart</h2>
      {cart.items.length === 0 ? (
        <p>Your cart is empty</p>
      ) : (
        <>
          <ul aria-label="Cart items">
            {cart.items.map((item) => (
              <li key={item.productId}>
                {item.name} × {item.quantity} — {formatPrice(item.price * item.quantity)}
              </li>
            ))}
          </ul>
          <p>Total: {formatPrice(total(cart))}</p>
        </>
      )}
    </section>
  );
}
