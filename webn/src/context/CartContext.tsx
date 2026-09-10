import React, { createContext, useContext, useState, useEffect, useMemo, ReactNode } from 'react';
import { CartItem, CartItemDetailed, Pizza, PizzaSize } from '../types/pizza';
import { PIZZAS } from '../data/pizzas';
import { fetchProducts } from '../utils/api';
import { getSavedBotUsername, saveBotUsername as persistBotUsername, triggerHaptic } from '../utils/telegram';

interface ToastState {
  id: number;
  message: string;
  type?: 'success' | 'info' | 'warning';
}

interface CartContextType {
  pizzas: Pizza[];
  refreshProducts: () => Promise<void>;
  cart: CartItem[];
  detailedCart: CartItemDetailed[];
  totalItemsCount: number;
  subtotal: number;
  deliveryFee: number;
  totalPrice: number;
  addToCart: (pizzaId: number, size: PizzaSize, qty?: number) => void;
  updateQty: (pizzaId: number, size: PizzaSize, newQty: number) => void;
  removeFromCart: (pizzaId: number, size: PizzaSize) => void;
  clearCart: () => void;
  toasts: ToastState[];
  showToast: (message: string, type?: 'success' | 'info' | 'warning') => void;
  removeToast: (id: number) => void;
  selectedPizzaForModal: Pizza | null;
  openPizzaModal: (pizza: Pizza) => void;
  closePizzaModal: () => void;
  botUsername: string;
  updateBotUsername: (username: string) => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const CART_STORAGE_KEY = 'pizzahouse_cart_v1';

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // Load initial cart from localStorage
  const [cart, setCart] = useState<CartItem[]>(() => {
    if (typeof window === 'undefined') return [];
    try {
      const saved = localStorage.getItem(CART_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          return parsed.filter(
            (item: any) =>
              typeof item.pizzaId === 'number' &&
              [25, 30, 35].includes(item.size) &&
              typeof item.qty === 'number' &&
              item.qty > 0
          );
        }
      }
    } catch (e) {
      console.error('Failed to parse saved cart:', e);
    }
    return [];
  });

  const [pizzas, setPizzas] = useState<Pizza[]>(PIZZAS);
  const [toasts, setToasts] = useState<ToastState[]>([]);
  const [selectedPizzaForModal, setSelectedPizzaForModal] = useState<Pizza | null>(null);
  const [botUsername, setBotUsernameState] = useState<string>(getSavedBotUsername);

  const refreshProducts = async () => {
    try {
      const live = await fetchProducts();
      if (live && live.length > 0) {
        setPizzas(live);
      }
    } catch (e) {
      console.warn('Failed to refresh products:', e);
    }
  };

  useEffect(() => {
    refreshProducts();
  }, []);

  // Sync cart to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {
      console.error('Failed to persist cart:', e);
    }
  }, [cart]);

  const updateBotUsername = (username: string) => {
    persistBotUsername(username);
    setBotUsernameState(username.replace(/^@/, '').trim());
  };

  const showToast = (message: string, type: 'success' | 'info' | 'warning' = 'success') => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev.slice(-2), { id, message, type }]); // keep max 3 toasts
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3200);
  };

  const removeToast = (id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const openPizzaModal = (pizza: Pizza) => {
    triggerHaptic('light');
    setSelectedPizzaForModal(pizza);
  };

  const closePizzaModal = () => {
    setSelectedPizzaForModal(null);
  };

  /**
   * Add to cart:
   * "Если одна и та же пицца добавлена с разными размерами, они должны быть отдельными позициями."
   */
  const addToCart = (pizzaId: number, size: PizzaSize, qty: number = 1) => {
    triggerHaptic('medium');
    const pizza = pizzas.find((p) => p.id === pizzaId) || PIZZAS.find((p) => p.id === pizzaId);
    if (!pizza) return;

    setCart((prev) => {
      const existingIndex = prev.findIndex(
        (item) => item.pizzaId === pizzaId && item.size === size
      );

      if (existingIndex > -1) {
        // Increase quantity, maximum 99
        const updated = [...prev];
        const newQty = Math.min(99, updated[existingIndex].qty + qty);
        updated[existingIndex] = { ...updated[existingIndex], qty: newQty };
        return updated;
      } else {
        // Add new position
        return [...prev, { pizzaId, size, qty: Math.min(99, Math.max(1, qty)) }];
      }
    });

    showToast(`🍕 «${pizza.name}» (${size} см) добавлена в корзину!`, 'success');
  };

  const updateQty = (pizzaId: number, size: PizzaSize, newQty: number) => {
    triggerHaptic('selection');
    if (newQty <= 0) {
      removeFromCart(pizzaId, size);
      return;
    }

    setCart((prev) =>
      prev.map((item) =>
        item.pizzaId === pizzaId && item.size === size
          ? { ...item, qty: Math.min(99, Math.max(1, newQty)) }
          : item
      )
    );
  };

  const removeFromCart = (pizzaId: number, size: PizzaSize) => {
    triggerHaptic('warning');
    const pizza = pizzas.find((p) => p.id === pizzaId) || PIZZAS.find((p) => p.id === pizzaId);
    setCart((prev) =>
      prev.filter((item) => !(item.pizzaId === pizzaId && item.size === size))
    );
    if (pizza) {
      showToast(`Позиция «${pizza.name}» удалена из корзины`, 'info');
    }
  };

  const clearCart = () => {
    setCart([]);
    try {
      localStorage.removeItem(CART_STORAGE_KEY);
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify([]));
    } catch (e) {
      console.error('Failed to clear cart storage:', e);
    }
  };

  // Detailed items with populated pizza information
  const detailedCart: CartItemDetailed[] = useMemo(() => {
    return cart
      .map((item) => {
        const pizza = pizzas.find((p) => p.id === item.pizzaId) || PIZZAS.find((p) => p.id === item.pizzaId);
        if (!pizza) return null;
        const itemPrice = pizza.prices[item.size] || 0;
        return {
          ...item,
          pizza,
          itemPrice,
          totalPrice: itemPrice * item.qty,
        };
      })
      .filter((item): item is CartItemDetailed => item !== null);
  }, [cart, pizzas]);

  const totalItemsCount = useMemo(() => {
    return cart.reduce((sum, item) => sum + item.qty, 0);
  }, [cart]);

  const subtotal = useMemo(() => {
    return detailedCart.reduce((sum, item) => sum + item.totalPrice, 0);
  }, [detailedCart]);

  const deliveryFee = 0; // "Бесплатно" as requested

  const totalPrice = subtotal + deliveryFee;

  return (
    <CartContext.Provider
      value={{
        pizzas,
        refreshProducts,
        cart,
        detailedCart,
        totalItemsCount,
        subtotal,
        deliveryFee,
        totalPrice,
        addToCart,
        updateQty,
        removeFromCart,
        clearCart,
        toasts,
        showToast,
        removeToast,
        selectedPizzaForModal,
        openPizzaModal,
        closePizzaModal,
        botUsername,
        updateBotUsername,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
