import React from 'react';
import { CATEGORIES } from '../data/pizzas';
import { CategoryId } from '../types/pizza';
import { triggerHaptic } from '../utils/telegram';

interface CategoryTabsProps {
  selectedCategory: CategoryId;
  onSelectCategory: (id: CategoryId) => void;
}

export const CategoryTabs: React.FC<CategoryTabsProps> = ({
  selectedCategory,
  onSelectCategory,
}) => {
  const handleSelect = (id: CategoryId) => {
    triggerHaptic('selection');
    onSelectCategory(id);
  };

  return (
    <div className="w-full overflow-x-auto no-scrollbar py-2 px-4 -mx-4 flex gap-2">
      {CATEGORIES.map((cat) => {
        const isSelected = selectedCategory === cat.id;
        return (
          <button
            key={cat.id}
            id={`category-tab-${cat.id}`}
            type="button"
            onClick={() => handleSelect(cat.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-2xl font-bold text-xs whitespace-nowrap transition-all active:scale-95 ${
              isSelected
                ? 'bg-amber-500 text-stone-950 shadow-md shadow-amber-500/20'
                : 'bg-stone-800/90 hover:bg-stone-800 text-stone-300 hover:text-white border border-stone-700/60'
            }`}
          >
            <span className="text-base">{cat.emoji}</span>
            <span>{cat.name}</span>
          </button>
        );
      })}
    </div>
  );
};
