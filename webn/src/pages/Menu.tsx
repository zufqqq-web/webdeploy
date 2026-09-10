import React, { useState } from 'react';
import { EXTRA_ITEMS } from '../data/pizzas';
import { Pizza, CategoryId } from '../types/pizza';
import { PizzaCard } from '../components/PizzaCard';
import { CategoryTabs } from '../components/CategoryTabs';
import { Search, Info, Plus } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { formatPrice } from '../utils/formatPrice';

interface MenuProps {
  initialCategory?: CategoryId;
}

export const Menu: React.FC<MenuProps> = ({ initialCategory = 'pizzas' }) => {
  const [selectedCategory, setSelectedCategory] = useState<CategoryId>(initialCategory);
  const [searchQuery, setSearchQuery] = useState('');
  const { openPizzaModal, showToast, pizzas } = useCart();

  // Filter pizzas
  const filteredPizzas = (pizzas || []).filter((pizza) => {
    const matchesQuery =
      pizza.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      pizza.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (pizza.ingredients || []).some((ing) => ing.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesQuery;
  });

  // Filter extra items
  const filteredExtras = EXTRA_ITEMS.filter((item) => {
    const matchesCategory = item.category === selectedCategory;
    const matchesQuery =
      item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesQuery;
  });

  return (
    <div className="space-y-4 pb-24">
      {/* Category selector */}
      <div className="sticky top-[61px] z-20 bg-stone-900/90 backdrop-blur-md pt-1 pb-2 border-b border-stone-800/80">
        <CategoryTabs
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-500" />
        <input
          id="menu-search-input"
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Поиск по меню и ингредиентам..."
          className="w-full bg-stone-850 border border-stone-800 focus:border-amber-500 rounded-2xl pl-10 pr-4 py-2.5 text-xs text-white placeholder:text-stone-500 outline-none transition-colors"
        />
        {searchQuery && (
          <button
            onClick={() => setSearchQuery('')}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-white text-xs px-1"
          >
            Очистить
          </button>
        )}
      </div>

      {/* Main Pizza Catalog */}
      {selectedCategory === 'pizzas' && (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs text-stone-400 font-semibold px-1">
            <span>Найдено пицц: {filteredPizzas.length}</span>
            <span>Размеры: 25 / 30 / 35 см</span>
          </div>

          {filteredPizzas.length === 0 ? (
            <div className="text-center py-12 space-y-2 bg-stone-850/50 rounded-3xl border border-stone-800">
              <span className="text-3xl">🔍</span>
              <p className="text-sm font-bold text-white">Пиццы не найдены</p>
              <p className="text-xs text-stone-400">
                Попробуйте изменить поисковый запрос
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              {filteredPizzas.map((pizza) => (
                <PizzaCard
                  key={pizza.id}
                  pizza={pizza}
                  onSelect={openPizzaModal}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Extra categories (Combos, Drinks, Desserts) */}
      {selectedCategory !== 'pizzas' && (
        <div className="space-y-3">
          <div className="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-2.5 text-xs text-amber-200">
            <Info className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
            <p>
              В текущей версии Telegram-бота deep link оформляет фирменные 6 пицц (Пепперони, Маргарита, 4 сыра, Гавайская, BBQ, Мясная). Дополнительные позиции можно добавить к заказу при подтверждении оператором.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {filteredExtras.map((item) => (
              <div
                key={item.id}
                className="bg-stone-850 rounded-3xl border border-stone-800 p-3.5 flex gap-3 items-center"
              >
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-20 h-20 rounded-2xl object-cover bg-stone-900 flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5">
                    <h4 className="font-extrabold text-sm text-white truncate">
                      {item.name}
                    </h4>
                    {item.badge && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400">
                        {item.badge}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-stone-400 line-clamp-2 mt-1">
                    {item.description}
                  </p>
                  <div className="flex items-center justify-between mt-2 pt-1 border-t border-stone-800">
                    <span className="font-extrabold text-xs text-amber-400">
                      {formatPrice(item.price)}
                    </span>
                    <button
                      onClick={() =>
                        showToast(`Позиция «${item.name}» будет добавлена оператором к заказу!`, 'info')
                      }
                      className="px-2.5 py-1 rounded-xl bg-stone-800 hover:bg-stone-750 text-stone-300 text-[11px] font-semibold border border-stone-700"
                    >
                      К заказу
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
