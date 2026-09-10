/**
 * Formats a number into Uzbek Sum format with non-breaking space separation
 * Example: 45000 -> "45 000 сум"
 */
export function formatPrice(price: number): string {
  if (typeof price !== 'number' || isNaN(price)) {
    return '0 сум';
  }
  const formatted = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  return `${formatted} сум`;
}
