import { CartItem } from '../types/pizza';
import { DEFAULT_BOT_USERNAME } from '../data/pizzas';

// Declare Telegram WebApp global interface
declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        ready: () => void;
        expand?: () => void;
        close?: () => void;
        openTelegramLink?: (url: string) => void;
        openLink?: (url: string) => void;
        setHeaderColor?: (color: string) => void;
        setBackgroundColor?: (color: string) => void;
        MainButton?: {
          text: string;
          color: string;
          textColor: string;
          isVisible: boolean;
          isActive: boolean;
          show: () => void;
          hide: () => void;
          enable: () => void;
          disable: () => void;
          onClick: (cb: () => void) => void;
          offClick: (cb: () => void) => void;
        };
        HapticFeedback?: {
          impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
          notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
          selectionChanged: () => void;
        };
        colorScheme?: 'light' | 'dark';
        themeParams?: Record<string, string>;
        initDataUnsafe?: {
          user?: {
            id: number;
            first_name: string;
            last_name?: string;
            username?: string;
          };
        };
      };
    };
  }
}

/**
 * Generates the precise payload string expected by bot.py
 * Format: m-<pizzaId>_<size>_<qty>[-<pizzaId>_<size>_<qty>]
 * Example: m-1_30_2-2_25_1
 */
export function generatePayload(cart: CartItem[]): string {
  if (!cart || cart.length === 0) {
    throw new Error('Корзина пуста');
  }

  // Validate each item
  for (const item of cart) {
    if (!item.pizzaId || typeof item.pizzaId !== 'number') {
      throw new Error(`Некорректный ID пиццы: ${item.pizzaId}`);
    }
    if (![25, 30, 35].includes(item.size)) {
      throw new Error(`Недопустимый размер: ${item.size}. Допустимы: 25, 30, 35`);
    }
    if (!item.qty || item.qty < 1 || item.qty > 99) {
      throw new Error(`Недопустимое количество: ${item.qty}. Допустимо от 1 до 99`);
    }
  }

  const itemsString = cart
    .map((item) => `${item.pizzaId}_${item.size}_${item.qty}`)
    .join('-');

  return `m-${itemsString}`;
}

/**
 * Generates the deep link for Telegram Bot
 * Example: https://t.me/PizzaHouseBot?start=m-1_30_2
 */
export function generateDeepLink(botUsername: string, cart: CartItem[]): string {
  const cleanUsername = (botUsername || DEFAULT_BOT_USERNAME).replace(/^@/, '').trim();
  const payload = generatePayload(cart);
  return `https://t.me/${cleanUsername}?start=${payload}`;
}

/**
 * Initializes Telegram WebApp if present
 */
export function initTelegramWebApp(): void {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;
    try {
      tg.ready();
      tg.expand?.();
      tg.setHeaderColor?.('#1c1917'); // stone-900
      tg.setBackgroundColor?.('#1c1917');
    } catch (e) {
      console.warn('Failed to initialize Telegram WebApp fully:', e);
    }
  }
}

/**
 * Checks if the app is currently running inside Telegram
 */
export function isRunningInTelegram(): boolean {
  return typeof window !== 'undefined' && Boolean(window.Telegram?.WebApp?.initDataUnsafe);
}

/**
 * Safe Haptic feedback triggers
 */
export function triggerHaptic(type: 'light' | 'medium' | 'heavy' | 'success' | 'warning' | 'error' | 'selection'): void {
  try {
    const haptic = window.Telegram?.WebApp?.HapticFeedback;
    if (!haptic) return;

    if (type === 'selection') {
      haptic.selectionChanged();
    } else if (['light', 'medium', 'heavy'].includes(type)) {
      haptic.impactOccurred(type as 'light' | 'medium' | 'heavy');
    } else if (['success', 'warning', 'error'].includes(type)) {
      haptic.notificationOccurred(type as 'success' | 'warning' | 'error');
    }
  } catch {
    // Ignore in non-Telegram environments
  }
}

/**
 * Opens Telegram Deep Link using Telegram WebApp API if available,
 * with standard browser fallbacks.
 */
export function openTelegramDeepLink(url: string): void {
  const tg = typeof window !== 'undefined' ? window.Telegram?.WebApp : undefined;

  if (tg?.openTelegramLink) {
    tg.openTelegramLink(url);
  } else {
    // Standard web browser fallback
    window.location.href = url;
  }
}

/**
 * Local storage helper to manage custom bot username (useful for homework testing!)
 */
const BOT_USERNAME_STORAGE_KEY = 'pizzahouse_bot_username';

export function getSavedBotUsername(): string {
  if (typeof window === 'undefined') return DEFAULT_BOT_USERNAME;
  const saved = localStorage.getItem(BOT_USERNAME_STORAGE_KEY);
  if (!saved || saved === 'PizzaHouseBot') return DEFAULT_BOT_USERNAME;
  return saved;
}

export function saveBotUsername(username: string): void {
  if (typeof window === 'undefined') return;
  const clean = username.replace(/^@/, '').trim();
  if (clean) {
    localStorage.setItem(BOT_USERNAME_STORAGE_KEY, clean);
  }
}
