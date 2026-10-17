import { describe, expect, it } from 'vitest';
import { formatPrice } from './cart';

describe('hidden: formatPrice', () => {
  it('uses Peruvian soles with two decimals', () => {
    expect(formatPrice(4.25)).toBe('S/ 4.25');
    expect(formatPrice(3)).toBe('S/ 3.00');
  });
});
