import React, { useState } from 'react';
import { Pizza } from '../types/pizza';
import { formatPrice } from '../utils/formatPrice';
import { Plus, Flame, Clock } from 'lucide-react';
import { useCart } from '../context/CartContext';

interface PizzaCardProps {
  pizza: Pizza;
  onSelect: (pizza: Pizza) => void;
}

export const PizzaCard: React.FC<PizzaCardProps> = ({ pizza, onSelect }) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const { cart } = useCart();

  // Find minimum price among sizes (25cm is the smallest size)
  const minPrice = pizza.prices[25] ?? Math.min(pizza.prices[25], pizza.prices[30], pizza.prices[35]);

  // Count how many of this pizza are in the cart across all sizes
  const cartCountForPizza = cart
    .filter((item) => item.pizzaId === pizza.id)
    .reduce((sum, item) => sum + item.qty, 0);

  return (
    <div
      id={`pizza-card-${pizza.id}`}
      onClick={() => onSelect(pizza)}
      className="group relative bg-stone-850 rounded-3xl border border-stone-800 hover:border-amber-500/50 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-xl hover:shadow-amber-500/5 active:scale-[0.98] flex flex-col justify-between"
    >
      {/* Image container */}
      <div className="relative w-full aspect-[4/3] bg-stone-900 overflow-hidden">
        {/* Skeleton shimmer while loading */}
        {!imageLoaded && (
          <div className="absolute inset-0 bg-stone-800 animate-pulse" />
        )}

        <img
          src={pizza.image}
          alt={pizza.name}
          loading="lazy"
          onLoad={() => setImageLoaded(true)}
          className={`w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          }`}
        />

        {/* Gradient shadow overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-stone-900 via-transparent to-black/30" />

        {/* Badge if present */}
        {pizza.badge && (
          <div className="absolute top-3 left-3 bg-stone-900/80 backdrop-blur-md px-2.5 py-1 rounded-full text-[11px] font-bold text-amber-400 border border-amber-500/30 flex items-center gap-1 shadow-md">
            <span>{pizza.badge}</span>
          </div>
        )}

        {/* In-cart indicator badge */}
        {cartCountForPizza > 0 && (
          <div className="absolute top-3 right-3 bg-amber-500 text-stone-950 px-2 py-0.5 rounded-full text-[11px] font-extrabold shadow-lg flex items-center gap-1 border border-amber-300">
            <span>В корзине: {cartCountForPizza}</span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-grow justify-between gap-3">
        <div>
          <div className="flex items-start justify-between gap-2 mb-1">
            <h3 className="font-extrabold text-base text-white group-hover:text-amber-400 transition-colors">
              {pizza.name}
            </h3>
            {pizza.calories && (
              <span className="text-[10px] text-stone-400 whitespace-nowrap pt-0.5">
                {pizza.calories} ккал
              </span>
            )}
          </div>

          <p className="text-xs text-stone-400 line-clamp-2 leading-relaxed">
            {pizza.description}
          </p>
        </div>

        {/* Price & Action button */}
        <div className="pt-2 border-t border-stone-800/80 flex items-center justify-between gap-2">
          <div>
            <span className="text-[10px] text-stone-400 font-semibold block uppercase tracking-wider">
              от
            </span>
            <span className="text-sm font-extrabold text-amber-400">
              {formatPrice(minPrice)}
            </span>
          </div>

          <button
            type="button"
            id={`pizza-choose-btn-${pizza.id}`}
            onClick={(e) => {
              e.stopPropagation();
              onSelect(pizza);
            }}
            className="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-bold text-xs flex items-center gap-1 shadow-md shadow-amber-500/10 transition-all active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Выбрать</span>
          </button>
        </div>
      </div>
    </div>
  );
};
