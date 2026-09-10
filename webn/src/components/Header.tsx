import React from 'react';
import { ShoppingBag, Bot, Sparkles } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { formatPrice } from '../utils/formatPrice';

interface HeaderProps {
  onOpenCart: () => void;
  onOpenBotConfig: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenCart, onOpenBotConfig }) => {
  const { totalItemsCount, totalPrice, botUsername } = useCart();

  return (
    <header className="sticky top-0 z-30 bg-stone-900/90 backdrop-blur-md border-b border-stone-800/80 px-4 py-3 transition-all">
      <div className="max-w-md mx-auto flex items-center justify-between">
        {/* Logo & Brand */}
        <div className="flex items-center gap-2.5">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-600 to-amber-500 flex items-center justify-center text-xl shadow-lg shadow-amber-600/20 border border-amber-400/30">
            🍕
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h1 className="text-lg font-extrabold tracking-tight text-white leading-none">
                PizzaHouse
              </h1>
              <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30">
                <Sparkles className="w-2.5 h-2.5" /> Mini App
              </span>
            </div>
            <p className="text-[11px] text-stone-400 font-medium tracking-wide mt-0.5">
              Горячая пицца. Быстрая доставка.
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* Bot Username Button / Config */}
          <button
            id="header-bot-config-btn"
            onClick={onOpenBotConfig}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-stone-800 hover:bg-stone-750 text-stone-300 hover:text-white border border-stone-700/80 text-xs font-medium transition-colors"
            title="Настройки Telegram бота"
          >
            <Bot className="w-3.5 h-3.5 text-sky-400" />
            <span className="max-w-[75px] truncate">@{botUsername}</span>
          </button>

          {/* Cart Icon with Counter Badge */}
          <button
            id="header-cart-btn"
            onClick={onOpenCart}
            className="relative p-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-bold shadow-md shadow-amber-500/20 transition-all active:scale-95"
            aria-label="Корзина"
          >
            <ShoppingBag className="w-4 h-4" />
            {totalItemsCount > 0 && (
              <span className="absolute -top-1.5 -right-1.5 min-w-5 h-5 px-1 bg-red-600 text-white rounded-full text-[11px] font-bold flex items-center justify-center border-2 border-stone-900 animate-pulse">
                {totalItemsCount > 99 ? '99+' : totalItemsCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
