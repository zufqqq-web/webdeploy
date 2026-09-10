import React from 'react';
import { Minus, Plus } from 'lucide-react';
import { triggerHaptic } from '../utils/telegram';

interface QuantitySelectorProps {
  quantity: number;
  onQuantityChange: (newQty: number) => void;
  min?: number;
  max?: number;
  compact?: boolean;
}

export const QuantitySelector: React.FC<QuantitySelectorProps> = ({
  quantity,
  onQuantityChange,
  min = 1,
  max = 99,
  compact = false,
}) => {
  const handleDecrease = () => {
    if (quantity > min) {
      triggerHaptic('selection');
      onQuantityChange(quantity - 1);
    }
  };

  const handleIncrease = () => {
    if (quantity < max) {
      triggerHaptic('selection');
      onQuantityChange(quantity + 1);
    }
  };

  if (compact) {
    return (
      <div className="inline-flex items-center bg-stone-850 rounded-xl border border-stone-700/70 p-1">
        <button
          type="button"
          onClick={handleDecrease}
          disabled={quantity <= min}
          aria-label="Уменьшить количество"
          className="w-7 h-7 flex items-center justify-center rounded-lg bg-stone-800 text-stone-300 hover:text-white disabled:opacity-40 disabled:hover:text-stone-300 transition-colors active:scale-90"
        >
          <Minus className="w-3.5 h-3.5" />
        </button>
        <span className="w-8 text-center text-xs font-bold text-white tabular-nums">
          {quantity}
        </span>
        <button
          type="button"
          onClick={handleIncrease}
          disabled={quantity >= max}
          aria-label="Увеличить количество"
          className="w-7 h-7 flex items-center justify-center rounded-lg bg-stone-800 text-stone-300 hover:text-white disabled:opacity-40 disabled:hover:text-stone-300 transition-colors active:scale-90"
        >
          <Plus className="w-3.5 h-3.5" />
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-between bg-stone-800/90 rounded-2xl border border-stone-700/80 p-1.5">
      <button
        type="button"
        id="qty-decrease-btn"
        onClick={handleDecrease}
        disabled={quantity <= min}
        aria-label="Уменьшить"
        className="w-10 h-10 flex items-center justify-center rounded-xl bg-stone-700/70 hover:bg-stone-700 text-stone-200 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all active:scale-90"
      >
        <Minus className="w-4 h-4" />
      </button>

      <div className="flex flex-col items-center">
        <span className="text-base font-extrabold text-white tabular-nums">
          {quantity}
        </span>
        <span className="text-[10px] text-stone-400 uppercase tracking-wider font-semibold">
          шт
        </span>
      </div>

      <button
        type="button"
        id="qty-increase-btn"
        onClick={handleIncrease}
        disabled={quantity >= max}
        aria-label="Увеличить"
        className="w-10 h-10 flex items-center justify-center rounded-xl bg-stone-700/70 hover:bg-stone-700 text-stone-200 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all active:scale-90"
      >
        <Plus className="w-4 h-4" />
      </button>
    </div>
  );
};
