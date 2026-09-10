import React from 'react';
import { PizzaSize } from '../types/pizza';
import { formatPrice } from '../utils/formatPrice';
import { triggerHaptic } from '../utils/telegram';

interface SizeSelectorProps {
  prices: Record<PizzaSize, number>;
  selectedSize: PizzaSize;
  onSelectSize: (size: PizzaSize) => void;
  weight?: Record<PizzaSize, string>;
}

const AVAILABLE_SIZES: PizzaSize[] = [25, 30, 35];

export const SizeSelector: React.FC<SizeSelectorProps> = ({
  prices,
  selectedSize,
  onSelectSize,
  weight,
}) => {
  const handleSizeClick = (size: PizzaSize) => {
    triggerHaptic('selection');
    onSelectSize(size);
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-xs font-semibold text-stone-300">
        <span>Размер пиццы</span>
        <span className="text-amber-400 font-bold">
          {selectedSize} см {weight ? `• ${weight[selectedSize]}` : ''}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2">
        {AVAILABLE_SIZES.map((size) => {
          const isSelected = selectedSize === size;
          const price = prices[size];

          return (
            <button
              key={size}
              id={`size-btn-${size}`}
              type="button"
              onClick={() => handleSizeClick(size)}
              className={`relative flex flex-col items-center justify-center p-2.5 rounded-2xl border transition-all active:scale-95 ${
                isSelected
                  ? 'bg-amber-500/15 border-amber-500 text-amber-300 shadow-md shadow-amber-500/10 ring-2 ring-amber-500/30'
                  : 'bg-stone-800/80 hover:bg-stone-800 border-stone-700/80 text-stone-300 hover:text-white'
              }`}
            >
              {/* Radio indicator circle */}
              <div className="flex items-center gap-1.5 mb-1">
                <div
                  className={`w-3.5 h-3.5 rounded-full flex items-center justify-center border transition-colors ${
                    isSelected
                      ? 'border-amber-400 bg-amber-500'
                      : 'border-stone-500 bg-transparent'
                  }`}
                >
                  {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-stone-950" />}
                </div>
                <span className="font-bold text-sm tracking-tight">{size} см</span>
              </div>

              {/* Price per size */}
              <span
                className={`text-xs font-semibold whitespace-nowrap ${
                  isSelected ? 'text-white' : 'text-stone-400'
                }`}
              >
                {formatPrice(price)}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
