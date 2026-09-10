import React from 'react';
import { Home, UtensilsCrossed, ShoppingBag } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { formatPrice } from '../utils/formatPrice';
import { triggerHaptic } from '../utils/telegram';

export type TabType = 'home' | 'menu' | 'cart';

interface BottomNavProps {
  currentTab: TabType;
  onChangeTab: (tab: TabType) => void;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  currentTab,
  onChangeTab,
}) => {
  const { totalItemsCount, totalPrice } = useCart();

  const handleTabClick = (tab: TabType) => {
    triggerHaptic('selection');
    onChangeTab(tab);
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-stone-900/95 backdrop-blur-xl border-t border-stone-800/90 px-4 py-2 pb-[max(0.5rem,env(safe-area-inset-bottom))]">
      <div className="max-w-md mx-auto grid grid-cols-3 gap-2">
        {/* Home */}
        <button
          id="nav-home-btn"
          type="button"
          onClick={() => handleTabClick('home')}
          className={`flex flex-col items-center justify-center py-2 px-1 rounded-2xl transition-all active:scale-95 ${
            currentTab === 'home'
              ? 'text-amber-400 bg-amber-500/10 font-bold'
              : 'text-stone-400 hover:text-stone-200 font-medium'
          }`}
        >
          <Home className="w-5 h-5 mb-1" />
          <span className="text-[11px] leading-none">Главная</span>
        </button>

        {/* Menu */}
        <button
          id="nav-menu-btn"
          type="button"
          onClick={() => handleTabClick('menu')}
          className={`flex flex-col items-center justify-center py-2 px-1 rounded-2xl transition-all active:scale-95 ${
            currentTab === 'menu'
              ? 'text-amber-400 bg-amber-500/10 font-bold'
              : 'text-stone-400 hover:text-stone-200 font-medium'
          }`}
        >
          <UtensilsCrossed className="w-5 h-5 mb-1" />
          <span className="text-[11px] leading-none">Меню</span>
        </button>

        {/* Cart */}
        <button
          id="nav-cart-btn"
          type="button"
          onClick={() => handleTabClick('cart')}
          className={`relative flex flex-col items-center justify-center py-2 px-1 rounded-2xl transition-all active:scale-95 ${
            currentTab === 'cart'
              ? 'text-amber-400 bg-amber-500/10 font-bold'
              : 'text-stone-400 hover:text-stone-200 font-medium'
          }`}
        >
          <div className="relative">
            <ShoppingBag className="w-5 h-5 mb-1" />
            {totalItemsCount > 0 && (
              <span className="absolute -top-1 -right-2.5 min-w-4 h-4 px-1 rounded-full bg-amber-500 text-stone-950 text-[10px] font-extrabold flex items-center justify-center border border-stone-900">
                {totalItemsCount}
              </span>
            )}
          </div>
          <span className="text-[11px] leading-none">
            {totalItemsCount > 0 ? formatPrice(totalPrice) : 'Корзина'}
          </span>
        </button>
      </div>
    </nav>
  );
};
