import React, { useState } from 'react';
import { ShoppingBag, ArrowRight, Trash2, ShieldCheck, Sparkles, ExternalLink, Bot, Globe, CheckCircle2 } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { CartItemRow } from '../components/CartItem';
import { formatPrice } from '../utils/formatPrice';
import { generateDeepLink, openTelegramDeepLink, triggerHaptic } from '../utils/telegram';
import { submitWebOrder } from '../utils/api';
import { OrderLoadingModal } from '../components/OrderLoadingModal';

interface CartProps {
  onNavigateToMenu: () => void;
  onOpenBotConfig: () => void;
}

export const Cart: React.FC<CartProps> = ({ onNavigateToMenu, onOpenBotConfig }) => {
  const {
    cart,
    detailedCart,
    totalItemsCount,
    subtotal,
    deliveryFee,
    totalPrice,
    updateQty,
    removeFromCart,
    clearCart,
    botUsername,
    showToast,
  } = useCart();

  const [isOpeningTelegram, setIsOpeningTelegram] = useState(false);
  const [generatedUrl, setGeneratedUrl] = useState('');
  const [isOrderCompleted, setIsOrderCompleted] = useState(false);
  const [completedOrderNum, setCompletedOrderNum] = useState<number | null>(null);

  // Web order modal
  const [isWebOrderModalOpen, setIsWebOrderModalOpen] = useState(false);
  const [clientName, setClientName] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [comment, setComment] = useState('');
  const [isSubmittingWeb, setIsSubmittingWeb] = useState(false);

  const handleOrder = () => {
    if (cart.length === 0) {
      showToast('Корзина пуста. Выберите пиццу!', 'warning');
      return;
    }

    try {
      triggerHaptic('heavy');
      // Generate the exact deep link according to bot.py spec
      const url = generateDeepLink(botUsername, cart);
      setGeneratedUrl(url);
      setIsOpeningTelegram(true);
      setIsOrderCompleted(true);

      // Permanently clear cart from memory and localStorage
      clearCart();

      // Give a brief moment for the user to see "🚀 Открываем Telegram...", then trigger link
      setTimeout(() => {
        openTelegramDeepLink(url);
      }, 700);
    } catch (err: any) {
      showToast(err.message || 'Ошибка формирования заказа', 'warning');
    }
  };

  const handleWebSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!clientName.trim() || !phone.trim() || !address.trim()) {
      showToast('Пожалуйста, заполните все обязательные поля', 'warning');
      return;
    }

    setIsSubmittingWeb(true);
    triggerHaptic('heavy');

    const items = detailedCart.map((item) => ({
      product_id: item.pizzaId,
      name: item.pizza.name,
      size: item.size,
      qty: item.qty,
      price: item.itemPrice,
      line_total: item.totalPrice,
    }));

    const res = await submitWebOrder({
      client_name: clientName.trim(),
      phone: phone.trim(),
      address: address.trim(),
      comment: comment.trim(),
      items,
    });

    setIsSubmittingWeb(false);

    if (res.success && res.order_id) {
      setCompletedOrderNum(res.order_id);
      setIsOrderCompleted(true);
      setIsWebOrderModalOpen(false);
      clearCart();
      showToast(`✅ Заказ №${res.order_id} успешно оформлен!`, 'success');
    } else {
      showToast(res.error || 'Ошибка при оформлении заказа', 'warning');
    }
  };

  const handleManualOpenLink = () => {
    if (generatedUrl) {
      openTelegramDeepLink(generatedUrl);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="pb-24 pt-8 text-center space-y-5 max-w-sm mx-auto">
        <div
          className={`w-24 h-24 mx-auto rounded-full flex items-center justify-center text-4xl shadow-inner transition-colors ${
            isOrderCompleted
              ? 'bg-emerald-500/15 border border-emerald-500/30 text-emerald-400'
              : 'bg-stone-850 border border-stone-800'
          }`}
        >
          {isOrderCompleted ? '✅' : '🛒'}
        </div>

        <div className="space-y-1.5">
          <h2 className="text-xl font-extrabold text-white">
            {isOrderCompleted ? 'Заказ передан в бота!' : 'Ваша корзина пуста'}
          </h2>
          <p className="text-xs text-stone-400 leading-relaxed">
            {isOrderCompleted
              ? 'Корзина успешно очищена. Бот формирует ваш заказ — вы можете вернуться в меню для нового выбора.'
              : 'Кажется, вы ещё не выбрали свою любимую пиццу. Загляните в меню — там много вкусного!'}
          </p>
        </div>

        <button
          id="cart-empty-go-menu-btn"
          onClick={onNavigateToMenu}
          className="w-full py-3.5 px-6 rounded-2xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-black text-sm flex items-center justify-center gap-2 shadow-lg shadow-amber-500/20 active:scale-95 transition-all"
        >
          <span>Перейти в меню</span>
          <ArrowRight className="w-4 h-4" />
        </button>

        {/* Telegram Redirect Modal */}
        <OrderLoadingModal
          isOpen={isOpeningTelegram}
          deepLinkUrl={generatedUrl}
          onManualOpen={handleManualOpenLink}
          onClose={() => setIsOpeningTelegram(false)}
        />
      </div>
    );
  }

  return (
    <div className="space-y-5 pb-28">
      {/* Top Header Controls */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-black text-white flex items-center gap-2">
            <span>Корзина</span>
            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
              {totalItemsCount} {totalItemsCount === 1 ? 'позиция' : totalItemsCount < 5 ? 'позиции' : 'позиций'}
            </span>
          </h2>
          <p className="text-xs text-stone-400 mt-0.5">
            Проверьте состав и выбранные размеры
          </p>
        </div>

        <button
          id="clear-cart-btn"
          onClick={() => {
            if (window.confirm('Очистить корзину?')) {
              clearCart();
            }
          }}
          className="flex items-center gap-1 text-xs text-stone-400 hover:text-red-400 font-semibold px-2 py-1 rounded-lg hover:bg-stone-850 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Очистить</span>
        </button>
      </div>

      {/* Cart Items List */}
      <div className="space-y-3">
        {detailedCart.map((item) => (
          <CartItemRow
            key={`${item.pizzaId}_${item.size}`}
            item={item}
            onUpdateQty={(newQty) => updateQty(item.pizzaId, item.size, newQty)}
            onRemove={() => removeFromCart(item.pizzaId, item.size)}
          />
        ))}
      </div>

      {/* Delivery and Bot Info Banner */}
      <div className="bg-stone-850 border border-stone-800 rounded-3xl p-4 space-y-3">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2 text-stone-300">
            <Bot className="w-4 h-4 text-sky-400" />
            <span>Интеграция с ботом:</span>
          </div>
          <button
            onClick={onOpenBotConfig}
            className="font-mono text-amber-400 font-bold hover:underline"
          >
            @{botUsername} (изменить)
          </button>
        </div>

        <div className="flex items-center gap-2 text-xs text-stone-400 pt-2 border-t border-stone-800">
          <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>Бот автоматически проверит актуальную стоимость позиций по ТЗ.</span>
        </div>
      </div>

      {/* Bill Breakdown */}
      <div className="bg-stone-850/70 border border-stone-800 rounded-3xl p-4 space-y-2.5">
        <div className="flex items-center justify-between text-xs text-stone-300">
          <span>Подытог</span>
          <span className="font-semibold">{formatPrice(subtotal)}</span>
        </div>

        <div className="flex items-center justify-between text-xs text-stone-300">
          <div className="flex items-center gap-1.5">
            <span>Доставка</span>
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">
              Акция
            </span>
          </div>
          <span className="font-semibold text-emerald-400">Бесплатно</span>
        </div>

        <div className="pt-2 border-t border-stone-750 flex items-center justify-between">
          <span className="text-sm font-bold text-white">Итого к оплате</span>
          <span className="text-lg font-black text-amber-400">
            {formatPrice(totalPrice)}
          </span>
        </div>
      </div>

      {/* Order Buttons */}
      <div className="space-y-2.5">
        <button
          id="checkout-order-btn"
          onClick={handleOrder}
          className="w-full py-4 px-6 rounded-2xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-black text-base flex items-center justify-center gap-2.5 shadow-xl shadow-amber-500/30 active:scale-[0.98] transition-all"
        >
          <span>🚀 Заказать через Telegram</span>
          <span className="text-stone-800">•</span>
          <span>{formatPrice(totalPrice)}</span>
        </button>

        <button
          id="checkout-web-order-btn"
          onClick={() => setIsWebOrderModalOpen(true)}
          className="w-full py-3.5 px-6 rounded-2xl bg-stone-800 hover:bg-stone-750 text-white font-bold text-sm flex items-center justify-center gap-2 border border-stone-700 active:scale-[0.98] transition-all"
        >
          <Globe className="w-4 h-4 text-amber-400" />
          <span>Оформить заказ на сайте</span>
        </button>

        <p className="text-[11px] text-center text-stone-500 leading-tight">
          Выберите удобный способ: через Telegram-бота или напрямую через сайт
        </p>
      </div>

      {/* Web Order Modal */}
      {isWebOrderModalOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-stone-900 border border-stone-800 rounded-3xl p-6 w-full max-w-md shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-stone-800 pb-3">
              <h3 className="text-lg font-black text-white flex items-center gap-2">
                <span>📝</span> Оформление на сайте
              </h3>
              <button
                onClick={() => setIsWebOrderModalOpen(false)}
                className="text-stone-400 hover:text-white text-lg font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleWebSubmit} className="space-y-3">
              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-stone-400 mb-1">
                  Ваше имя *
                </label>
                <input
                  type="text"
                  required
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                  placeholder="Иван"
                  className="w-full bg-stone-800 border border-stone-700 focus:border-amber-500 rounded-xl px-3.5 py-2.5 text-sm text-white outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-stone-400 mb-1">
                  Телефон *
                </label>
                <input
                  type="tel"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+998 90 123 45 67"
                  className="w-full bg-stone-800 border border-stone-700 focus:border-amber-500 rounded-xl px-3.5 py-2.5 text-sm text-white outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-stone-400 mb-1">
                  Адрес доставки *
                </label>
                <input
                  type="text"
                  required
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Улица, дом, квартира"
                  className="w-full bg-stone-800 border border-stone-700 focus:border-amber-500 rounded-xl px-3.5 py-2.5 text-sm text-white outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-stone-400 mb-1">
                  Комментарий
                </label>
                <textarea
                  rows={2}
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Домофон, подъезд или пожелания"
                  className="w-full bg-stone-800 border border-stone-700 focus:border-amber-500 rounded-xl px-3.5 py-2 text-sm text-white outline-none"
                />
              </div>

              <div className="pt-2 flex items-center justify-between text-xs text-stone-400 border-t border-stone-800">
                <span>Сумма заказа:</span>
                <span className="text-base font-extrabold text-amber-400">{formatPrice(totalPrice)}</span>
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsWebOrderModalOpen(false)}
                  className="flex-1 py-3 rounded-xl bg-stone-800 text-stone-300 font-bold text-xs"
                >
                  Отмена
                </button>
                <button
                  type="submit"
                  disabled={isSubmittingWeb}
                  className="flex-1 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-black text-xs shadow-lg shadow-amber-500/20"
                >
                  {isSubmittingWeb ? 'Отправка...' : 'Подтвердить заказ'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Telegram Redirect Modal */}
      <OrderLoadingModal
        isOpen={isOpeningTelegram}
        deepLinkUrl={generatedUrl}
        onManualOpen={handleManualOpenLink}
        onClose={() => setIsOpeningTelegram(false)}
      />
    </div>
  );
};
