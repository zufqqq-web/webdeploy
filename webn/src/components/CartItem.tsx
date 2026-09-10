import React from 'react';
import { Trash2 } from 'lucide-react';
import { CartItemDetailed } from '../types/pizza';
import { formatPrice } from '../utils/formatPrice';
import { QuantitySelector } from './QuantitySelector';

interface CartItemProps {
  item: CartItemDetailed;
  onUpdateQty: (newQty: number) => void;
  onRemove: () => void;
}

export const CartItemRow: React.FC<CartItemProps> = ({
  item,
  onUpdateQty,
  onRemove,
}) => {
  return (
    <div
      id={`cart-item-${item.pizzaId}-${item.size}`}
      className="bg-stone-850 border border-stone-800 rounded-3xl p-3.5 flex gap-3.5 items-center transition-all hover:border-stone-700"
    >
      {/* Thumbnail */}
      <img
        src={item.pizza.image}
        alt={item.pizza.name}
        className="w-16 h-16 rounded-2xl object-cover bg-stone-900 border border-stone-800 flex-shrink-0"
      />

      {/* Item info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-1">
          <h4 className="font-extrabold text-sm text-white truncate">
            🍕 {item.pizza.name}
          </h4>
          <button
            type="button"
            id={`remove-cart-item-${item.pizzaId}-${item.size}`}
            onClick={onRemove}
            className="text-stone-500 hover:text-red-400 p-1 -mr-1 transition-colors"
            title="Удалить"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>

        {/* Size badge and single item price */}
        <div className="flex items-center gap-2 mt-0.5 text-xs text-stone-400">
          <span className="px-2 py-0.5 rounded-md bg-stone-800 text-amber-400 font-semibold text-[11px] border border-stone-750">
            {item.size} см
          </span>
          <span>{formatPrice(item.itemPrice)}</span>
        </div>

        {/* Controls and Total */}
        <div className="flex items-center justify-between mt-2.5 pt-2 border-t border-stone-800/80">
          <QuantitySelector
            compact
            quantity={item.qty}
            onQuantityChange={onUpdateQty}
          />

          <span className="text-sm font-extrabold text-white tabular-nums">
            {formatPrice(item.totalPrice)}
          </span>
        </div>
      </div>
    </div>
  );
};
