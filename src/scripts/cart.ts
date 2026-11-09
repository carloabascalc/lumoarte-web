// Carrito de la tienda. Guarda solo SKU y cantidad: nombres, precios y
// existencias se leen siempre del catálogo de la página, nunca de aquí.

const KEY = "lumo-cart-v1";
export const CART_EVENT = "lumo:cart";

export interface CartLine {
  sku: string;
  qty: number;
}

export function readCart(): CartLine[] {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter(
        (l): l is CartLine =>
          typeof l === "object" && l !== null && typeof l.sku === "string" && Number.isInteger(l.qty) && l.qty > 0,
      )
      .map((l) => ({ sku: l.sku, qty: l.qty }));
  } catch {
    return [];
  }
}

export function writeCart(lines: CartLine[]): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(lines.filter((l) => l.qty > 0)));
  } catch {
    // Sin almacenamiento (modo privado): el carrito dura lo que dure la página.
  }
  document.dispatchEvent(new CustomEvent(CART_EVENT));
}

/** Suma al carrito sin pasar de `max`. Devuelve la cantidad que quedó en ese renglón. */
export function addToCart(sku: string, qty: number, max: number): number {
  const lines = readCart();
  const line = lines.find((l) => l.sku === sku);
  const next = Math.min(max, (line?.qty ?? 0) + qty);
  if (line) line.qty = next;
  else lines.push({ sku, qty: next });
  writeCart(lines);
  return next;
}

export function setQty(sku: string, qty: number): void {
  const lines = readCart();
  const line = lines.find((l) => l.sku === sku);
  if (!line) return;
  line.qty = qty;
  writeCart(lines);
}

export function clearCart(): void {
  writeCart([]);
}

export const cartCount = (): number => readCart().reduce((n, l) => n + l.qty, 0);
