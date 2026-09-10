import React, { useState, useEffect } from 'react';
import { CartProvider, useCart } from './context/CartContext';
import { Header } from './components/Header';
import { BottomNav, TabType } from './components/BottomNav';
import { PizzaModal } from './components/PizzaModal';
import { BotConfigModal } from './components/BotConfigModal';
import { ToastContainer } from './components/Toast';
import { Home } from './pages/Home';
import { Menu } from './pages/Menu';
import { Cart } from './pages/Cart';
import { Pizza, CategoryId } from './types/pizza';
import { initTelegramWebApp } from './utils/telegram';

function PizzaApp() {
  const [currentTab, setCurrentTab] = useState<TabType>('home');
  const [menuInitialCategory, setMenuInitialCategory] = useState<CategoryId>('pizzas');
  const [isBotConfigOpen, setIsBotConfigOpen] = useState(false);
  const { selectedPizzaForModal, openPizzaModal, closePizzaModal } = useCart();

  // Initialize Telegram WebApp on mount
  useEffect(() => {
    initTelegramWebApp();
  }, []);

  const handleNavigateToMenu = (category: CategoryId = 'pizzas') => {
    setMenuInitialCategory(category);
    setCurrentTab('menu');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectPizza = (pizza: Pizza) => {
    openPizzaModal(pizza);
  };

  return (
    <div className="min-h-screen bg-stone-900 text-stone-100 flex flex-col font-['Plus_Jakarta_Sans',sans-serif]">
      {/* Toast notifications */}
      <ToastContainer />

      {/* Header */}
      <Header
        onOpenCart={() => {
          setCurrentTab('cart');
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        onOpenBotConfig={() => setIsBotConfigOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-md w-full mx-auto px-4 pt-4">
        {currentTab === 'home' && (
          <Home
            onSelectPizza={handleSelectPizza}
            onNavigateToMenu={handleNavigateToMenu}
          />
        )}

        {currentTab === 'menu' && (
          <Menu
            initialCategory={menuInitialCategory}
          />
        )}

        {currentTab === 'cart' && (
          <Cart
            onNavigateToMenu={() => handleNavigateToMenu('pizzas')}
            onOpenBotConfig={() => setIsBotConfigOpen(true)}
          />
        )}
      </main>

      {/* Sticky Mobile Bottom Navigation */}
      <BottomNav
        currentTab={currentTab}
        onChangeTab={(tab) => {
          setCurrentTab(tab);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
      />

      {/* Detail Pizza Modal (Bottom sheet) */}
      <PizzaModal
        pizza={selectedPizzaForModal}
        onClose={closePizzaModal}
      />

      {/* Bot Username Configuration Modal */}
      <BotConfigModal
        isOpen={isBotConfigOpen}
        onClose={() => setIsBotConfigOpen(false)}
      />
    </div>
  );
}

export default function App() {
  return (
    <CartProvider>
      <PizzaApp />
    </CartProvider>
  );
}
