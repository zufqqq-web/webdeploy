import React from 'react';
import { CATEGORIES } from '../data/pizzas';
import { Pizza, CategoryId } from '../types/pizza';
import { PizzaCard } from '../components/PizzaCard';
import { CategoryTabs } from '../components/CategoryTabs';
import { formatPrice } from '../utils/formatPrice';
import { Flame, Clock, ShieldCheck, ArrowRight, Sparkles } from 'lucide-react';
import { useCart } from '../context/CartContext';

interface HomeProps {
  onSelectPizza: (pizza: Pizza) => void;
  onNavigateToMenu: (category?: CategoryId) => void;
}

export const Home: React.FC<HomeProps> = ({ onSelectPizza, onNavigateToMenu }) => {
  const { openPizzaModal, pizzas } = useCart();

  // Featured pizza for the Hero section (Пепперони - ID 1)
  const heroPizza = (pizzas && pizzas.length > 0)
    ? (pizzas.find((p) => p.id === 1) || pizzas[0])
    : { id: 1, name: 'Пепперони', description: '', ingredients: [], category: 'pizza', image: '', prices: { 25: 45000, 30: 60000, 35: 75000 } };
  const heroMinPrice = heroPizza.prices[25] ?? Math.min(heroPizza.prices[25] || 0, heroPizza.prices[30] || 0, heroPizza.prices[35] || 0);

  // Popular pizzas
  const popularPizzas = (pizzas || []).filter((p) => p.isPopular);

  return (
    <div className="space-y-6 pb-24">
      {/* Hero Banner Section */}
      <section className="relative overflow-hidden rounded-[32px] bg-gradient-to-b from-stone-850 to-stone-900 border border-stone-800 p-5 shadow-xl">
        <div className="flex items-center gap-2 text-amber-400 text-xs font-extrabold tracking-wide uppercase mb-3">
          <Flame className="w-4 h-4 text-amber-500 fill-amber-500" />
          <span>Популярное сегодня</span>
        </div>

        {/* Big featured pizza card */}
        <div className="relative rounded-2xl overflow-hidden bg-stone-950/80 border border-stone-800/80 mb-4 group">
          <div className="relative w-full aspect-[16/9] overflow-hidden">
            <img
              src={heroPizza.image}
              alt={heroPizza.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/40 to-transparent" />

            <div className="absolute top-3 left-3 bg-amber-500 text-stone-950 px-2.5 py-1 rounded-full text-xs font-black uppercase tracking-wider shadow-lg flex items-center gap-1">
              <Sparkles className="w-3 h-3" />
              <span>Хит №1</span>
            </div>
          </div>

          <div className="p-4 space-y-2">
            <div className="flex items-start justify-between gap-2">
              <h2 className="text-xl font-black text-white group-hover:text-amber-400 transition-colors">
                🍕 {heroPizza.name}
              </h2>
              <div className="text-right">
                <span className="text-[10px] text-stone-400 uppercase tracking-wider block">
                  цена от
                </span>
                <span className="text-base font-black text-amber-400">
                  {formatPrice(heroMinPrice)}
                </span>
              </div>
            </div>

            <p className="text-xs text-stone-300 leading-relaxed line-clamp-2">
              {heroPizza.description}
            </p>

            <div className="pt-2 flex items-center justify-between">
              <div className="flex items-center gap-2 text-stone-400 text-xs font-semibold">
                <span className="inline-block w-2 h-2 rounded-full bg-emerald-500" />
                <span>В наличии • 25 / 30 / 35 см</span>
              </div>

              <button
                id="hero-order-pizza-btn"
                onClick={() => openPizzaModal(heroPizza)}
                className="px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-extrabold text-xs flex items-center gap-1.5 shadow-lg shadow-amber-500/25 active:scale-95 transition-all"
              >
                <span>Заказать</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

        {/* Delivery Perks Pills */}
        <div className="grid grid-cols-3 gap-2 text-center">
          <div className="bg-stone-900/90 rounded-xl p-2 border border-stone-800">
            <Clock className="w-4 h-4 mx-auto text-amber-400 mb-1" />
            <span className="block text-[10px] font-bold text-white">30 минут</span>
            <span className="text-[9px] text-stone-400">Доставка</span>
          </div>
          <div className="bg-stone-900/90 rounded-xl p-2 border border-stone-800">
            <Flame className="w-4 h-4 mx-auto text-orange-400 mb-1" />
            <span className="block text-[10px] font-bold text-white">Из печи</span>
            <span className="text-[9px] text-stone-400">Всегда горячая</span>
          </div>
          <div className="bg-stone-900/90 rounded-xl p-2 border border-stone-800">
            <ShieldCheck className="w-4 h-4 mx-auto text-emerald-400 mb-1" />
            <span className="block text-[10px] font-bold text-white">0 сум</span>
            <span className="text-[9px] text-stone-400">Доставка</span>
          </div>
        </div>
      </section>

      {/* Categories quick horizontal list */}
      <section className="space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-extrabold text-white">Категории</h3>
          <button
            onClick={() => onNavigateToMenu('pizzas')}
            className="text-xs text-amber-400 hover:text-amber-300 font-bold flex items-center gap-0.5"
          >
            <span>Всё меню</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>
        <CategoryTabs
          selectedCategory="pizzas"
          onSelectCategory={(id) => onNavigateToMenu(id)}
        />
      </section>

      {/* Popular Pizzas Section */}
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-black text-white">
              Популярные пиццы
            </h3>
            <p className="text-xs text-stone-400">
              Любимый выбор наших гостей
            </p>
          </div>
          <button
            onClick={() => onNavigateToMenu('pizzas')}
            className="text-xs text-amber-400 hover:text-amber-300 font-bold flex items-center gap-0.5"
          >
            <span>Все 6 пицц</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          {popularPizzas.map((pizza) => (
            <PizzaCard
              key={pizza.id}
              pizza={pizza}
              onSelect={openPizzaModal}
            />
          ))}
        </div>
      </section>
    </div>
  );
};
