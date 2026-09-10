import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, ShoppingBag, Check } from 'lucide-react';
import { Pizza, PizzaSize } from '../types/pizza';
import { SizeSelector } from './SizeSelector';
import { QuantitySelector } from './QuantitySelector';
import { formatPrice } from '../utils/formatPrice';
import { useCart } from '../context/CartContext';

interface PizzaModalProps {
  pizza: Pizza | null;
  onClose: () => void;
}

export const PizzaModal: React.FC<PizzaModalProps> = ({ pizza, onClose }) => {
  const { addToCart } = useCart();
  const [selectedSize, setSelectedSize] = useState<PizzaSize>(30); // Default to standard 30cm
  const [quantity, setQuantity] = useState<number>(1);
  const [isAdded, setIsAdded] = useState(false);

  // Reset states when pizza changes
  useEffect(() => {
    if (pizza) {
      setSelectedSize(30);
      setQuantity(1);
      setIsAdded(false);
    }
  }, [pizza]);

  if (!pizza) return null;

  const currentUnitPrice = pizza.prices[selectedSize] || 0;
  const currentTotalPrice = currentUnitPrice * quantity;

  const handleAddToCart = () => {
    addToCart(pizza.id, selectedSize, quantity);
    setIsAdded(true);
    setTimeout(() => {
      setIsAdded(false);
      onClose();
    }, 450);
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm"
        />

        {/* Modal Container */}
        <motion.div
          initial={{ y: '100%', opacity: 0.5 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: '100%', opacity: 0 }}
          transition={{ type: 'spring', damping: 28, stiffness: 300 }}
          className="relative w-full max-w-md max-h-[90vh] bg-stone-900 border-t sm:border border-stone-800 rounded-t-[32px] sm:rounded-[32px] overflow-hidden flex flex-col shadow-2xl z-10"
        >
          {/* Close button */}
          <button
            id="close-pizza-modal-btn"
            onClick={onClose}
            className="absolute top-4 right-4 z-20 w-9 h-9 rounded-full bg-stone-900/80 backdrop-blur-md text-stone-300 hover:text-white flex items-center justify-center border border-stone-700/80 transition-colors"
            aria-label="Закрыть"
          >
            <X className="w-5 h-5" />
          </button>

          {/* Scrollable Body */}
          <div className="overflow-y-auto no-scrollbar pb-24">
            {/* Pizza Image */}
            <div className="relative w-full aspect-[16/10] bg-stone-950 overflow-hidden">
              <img
                src={pizza.image}
                alt={pizza.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-stone-900 via-transparent to-black/40" />

              {pizza.badge && (
                <div className="absolute bottom-3 left-4 bg-stone-900/85 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-amber-400 border border-amber-500/30">
                  {pizza.badge}
                </div>
              )}
            </div>

            {/* Pizza Info */}
            <div className="p-5 space-y-5">
              <div>
                <div className="flex items-baseline justify-between gap-2">
                  <h2 className="text-2xl font-extrabold text-white tracking-tight">
                    🍕 {pizza.name}
                  </h2>
                </div>

                <p className="text-sm text-stone-300 mt-2 leading-relaxed">
                  {pizza.description}
                </p>
              </div>

              {/* Composition / Ingredients List */}
              <div className="bg-stone-850/80 rounded-2xl p-4 border border-stone-800">
                <h3 className="text-xs font-bold text-stone-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
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

              {/* Size Selector */}
              <SizeSelector
                prices={pizza.prices}
                selectedSize={selectedSize}
                onSelectSize={setSelectedSize}
                weight={pizza.weight}
              />

              {/* Quantity Selector */}
              <div className="space-y-2">
                <span className="text-xs font-semibold text-stone-300 block">
                  Количество
                </span>
                <QuantitySelector
                  quantity={quantity}
                  onQuantityChange={setQuantity}
                />
              </div>

              {/* Calculated Price Breakdown */}
              <div className="bg-stone-800/60 rounded-2xl p-3 border border-stone-750 flex items-center justify-between text-xs">
                <span className="text-stone-400">
                  {formatPrice(currentUnitPrice)} × {quantity}
                </span>
                <span className="text-sm font-extrabold text-white">
                  = {formatPrice(currentTotalPrice)}
                </span>
              </div>
            </div>
          </div>

          {/* Sticky Bottom Action Bar */}
          <div className="absolute bottom-0 left-0 right-0 p-4 bg-stone-900/95 backdrop-blur-md border-t border-stone-800 flex items-center gap-3">
            <button
              id="add-to-cart-submit-btn"
              onClick={handleAddToCart}
              className={`flex-1 py-3.5 px-5 rounded-2xl font-extrabold text-sm flex items-center justify-center gap-2 shadow-lg transition-all active:scale-95 ${
                isAdded
                  ? 'bg-emerald-500 text-white'
                  : 'bg-amber-500 hover:bg-amber-400 text-stone-950 shadow-amber-500/25'
              }`}
            >
              {isAdded ? (
                <>
                  <Check className="w-5 h-5 animate-bounce" />
                  <span>Добавлено!</span>
                </>
              ) : (
                <>
                  <ShoppingBag className="w-4 h-4" />
                  <span>🛒 Добавить в корзину • {formatPrice(currentTotalPrice)}</span>
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
