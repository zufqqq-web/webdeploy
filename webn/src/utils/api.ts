import { Pizza } from '../types/pizza';
import { PIZZAS } from '../data/pizzas';

export async function fetchProducts(): Promise<Pizza[]> {
  try {
    const res = await fetch('/api/products');
    if (!res.ok) {
      throw new Error(`Failed to fetch: ${res.status}`);
    }
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      // Нормализуем данные, если нужно
      return data.map((item: any) => ({
        id: Number(item.id),
        name: item.name,
        description: item.description || '',
        ingredients: Array.isArray(item.ingredients) ? item.ingredients : [],
        category: item.category || 'pizzas',
        image: item.image || 'https://placehold.co/800x600/png?text=Pizza',
        prices: {
          25: Number(item.prices?.[25] ?? item.prices?.['25'] ?? item.price_25 ?? 0),
          30: Number(item.prices?.[30] ?? item.prices?.['30'] ?? item.price_30 ?? 0),
          35: Number(item.prices?.[35] ?? item.prices?.['35'] ?? item.price_35 ?? 0),
        },
        isPopular: item.isPopular ?? (item.id === 1 || item.id === 3),
        badge: item.badge ?? (item.id === 1 ? '🔥 Хит продаж' : undefined),
      }));
    }
    return PIZZAS;
  } catch (err) {
    console.warn('API /api/products unavailable, using local fallback:', err);
    return PIZZAS;
  }
}

export interface WebOrderPayload {
  client_name: string;
  phone: string;
  address: string;
  comment?: string;
  items: Array<{
    product_id: number;
    name: string;
    size: number;
    qty: number;
    price: number;
    line_total: number;
  }>;
}

export async function submitWebOrder(payload: WebOrderPayload): Promise<{ success: boolean; order_id?: number; error?: string }> {
  try {
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      return { success: false, error: data.error || 'Ошибка оформления заказа' };
    }

    return { success: true, order_id: data.order_id };
  } catch (err: any) {
    return { success: false, error: err.message || 'Ошибка сети' };
  }
}
