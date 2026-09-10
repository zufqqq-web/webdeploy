import React, { useState } from 'react';
import { ArrowLeft, ShoppingBag, Check } from 'lucide-react';
import { Pizza, PizzaSize } from '../types/pizza';
import { SizeSelector } from '../components/SizeSelector';
import { QuantitySelector } from '../components/QuantitySelector';
import { formatPrice } from '../utils/formatPrice';
import { useCart } from '../context/CartContext';

interface PizzaDetailsProps {
  pizza: Pizza;
  onBack: () => void;
}

export const PizzaDetails: React.FC<PizzaDetailsProps> = ({ pizza, onBack }) => {
  const { addToCart } = useCart();
  const [selectedSize, setSelectedSize] = useState<PizzaSize>(30);
  const [quantity, setQuantity] = useState<number>(1);
  const [isAdded, setIsAdded] = useState(false);

  const currentUnitPrice = pizza.prices[selectedSize] || 0;
  const currentTotalPrice = currentUnitPrice * quantity;

  const handleAddToCart = () => {
    addToCart(pizza.id, selectedSize, quantity);
    setIsAdded(true);
    setTimeout(() => {
      setIsAdded(false);
      onBack();
    }, 500);
  };

  return (
    <div className="pb-28 space-y-5">
      {/* Header back */}
      <button
        onClick={onBack}
        className="inline-flex items-center gap-2 text-xs font-bold text-stone-300 hover:text-white px-3 py-2 rounded-xl bg-stone-850 border border-stone-800 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Назад в каталог</span>
      </button>

      {/* Image */}
      <div className="relative w-full aspect-[4/3] rounded-3xl overflow-hidden bg-stone-900 border border-stone-800 shadow-xl">
        <img
          src={pizza.image}
          alt={pizza.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-stone-900 via-transparent to-transparent" />
        {pizza.badge && (
          <div className="absolute top-4 left-4 bg-stone-900/80 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-amber-400 border border-amber-500/30">
            {pizza.badge}
          </div>
        )}
      </div>

      {/* Title & description */}
      <div className="space-y-2">
        <h1 className="text-2xl font-black text-white">
          🍕 {pizza.name}
        </h1>
        <p className="text-sm text-stone-300 leading-relaxed">
          {pizza.description}
        </p>
      </div>

      {/* Composition / Ingredients */}
      <div className="bg-stone-850 rounded-2xl p-4 border border-stone-800 space-y-2">
        <h3 className="text-xs font-bold text-stone-400 uppercase tracking-wider flex items-center gap-1.5">
          <span>🥫</span> Состав:
        </h3>
        <ul className="space-y-1.5 text-xs text-stone-300">
          {pizza.ingredients.map((ingredient, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="text-amber-500 font-bold">•</span>
              <span>{ingredient}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Size selector */}
      <SizeSelector
        prices={pizza.prices}
        selectedSize={selectedSize}
        onSelectSize={setSelectedSize}
        weight={pizza.weight}
      />

      {/* Quantity */}
      <div className="space-y-1.5">
        <span className="text-xs font-semibold text-stone-300 block">
          Количество:
        </span>
        <QuantitySelector
          quantity={quantity}
          onQuantityChange={setQuantity}
        />
      </div>

      {/* Dynamic calculation banner */}
      <div className="bg-stone-800/80 rounded-2xl p-3 border border-stone-750 flex items-center justify-between text-xs">
        <span className="text-stone-400">
          {formatPrice(currentUnitPrice)} × {quantity}
        </span>
        <span className="text-sm font-extrabold text-white">
          = {formatPrice(currentTotalPrice)}
        </span>
      </div>

      {/* Add button */}
      <button
        onClick={handleAddToCart}
        className={`w-full py-4 px-6 rounded-2xl font-black text-sm flex items-center justify-center gap-2 shadow-xl transition-all active:scale-95 ${
          isAdded
            ? 'bg-emerald-500 text-white'
            : 'bg-amber-500 hover:bg-amber-400 text-stone-950 shadow-amber-500/20'
        }`}
      >
        {isAdded ? (
          <>
            <Check className="w-5 h-5" />
            <span>Добавлено в корзину!</span>
          </>
        ) : (
          <>
            <ShoppingBag className="w-4 h-4" />
            <span>🛒 Добавить в корзину • {formatPrice(currentTotalPrice)}</span>
          </>
        )}
      </button>
    </div>
  );
};
