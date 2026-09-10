export type PizzaSize = 25 | 30 | 35;

export interface Pizza {
  id: number;
  name: string;
  description: string;
  ingredients: string[];
  category: string;
  image: string;
  prices: Record<PizzaSize, number>;
  calories?: number;
  weight?: Record<PizzaSize, string>;
  isPopular?: boolean;
  badge?: string;
}

export interface ExtraItem {
  id: string;
  name: string;
  description: string;
  category: 'combos' | 'drinks' | 'desserts';
  image: string;
  price: number;
  badge?: string;
}

export interface CartItem {
  pizzaId: number;
  size: PizzaSize;
  qty: number;
}

export interface CartItemDetailed extends CartItem {
  pizza: Pizza;
  itemPrice: number;
  totalPrice: number;
}

export type CategoryId = 'all' | 'pizzas' | 'combos' | 'drinks' | 'desserts';

export interface Category {
  id: CategoryId;
  name: string;
  icon: string;
  emoji: string;
}
