import React, { useState } from 'react';
import { X, Bot, Check, AlertCircle, RefreshCw } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { DEFAULT_BOT_USERNAME } from '../data/pizzas';

interface BotConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const BotConfigModal: React.FC<BotConfigModalProps> = ({ isOpen, onClose }) => {
  const { botUsername, updateBotUsername } = useCart();
  const [usernameInput, setUsernameInput] = useState(botUsername);
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const clean = usernameInput.replace(/^@/, '').trim();
    if (clean) {
      updateBotUsername(clean);
      setSavedSuccess(true);
      setTimeout(() => {
        setSavedSuccess(false);
        onClose();
      }, 700);
    }
  };

  const handleReset = () => {
    setUsernameInput(DEFAULT_BOT_USERNAME);
    updateBotUsername(DEFAULT_BOT_USERNAME);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-md bg-stone-900 border border-stone-800 rounded-3xl p-6 shadow-2xl space-y-4">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-stone-400 hover:text-white p-1 rounded-full"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-sky-500/10 text-sky-400 border border-sky-500/30 flex items-center justify-center">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-extrabold text-base text-white">
              Telegram Бот для заказа
            </h3>
            <p className="text-xs text-stone-400">
              Настройка @username для передачи deep link
            </p>
          </div>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-stone-300 block">
              Username вашего Telegram-бота:
            </label>
            <div className="relative">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-stone-500 font-bold text-sm">
                @
              </span>
              <input
                type="text"
                value={usernameInput}
                onChange={(e) => setUsernameInput(e.target.value.replace(/^@/, ''))}
                placeholder="absurddddbot"
                className="w-full bg-stone-850 border border-stone-750 focus:border-amber-500 rounded-2xl pl-8 pr-4 py-3 text-sm text-white font-medium outline-none transition-colors"
              />
            </div>
            <p className="text-[11px] text-stone-400">
              По умолчанию: <span className="text-amber-400">@{DEFAULT_BOT_USERNAME}</span>. Вы можете указать username своего бота из домашнего задания (bot.py).
            </p>
          </div>

          <div className="p-3 bg-stone-800/60 rounded-2xl border border-stone-750 text-xs text-stone-300 space-y-1">
            <div className="flex items-center gap-1.5 font-semibold text-amber-400">
              <AlertCircle className="w-3.5 h-3.5" />
              <span>Формат deep link (по ТЗ):</span>
            </div>
            <code className="block p-2 bg-stone-950 rounded-xl text-[11px] text-amber-300/90 font-mono break-all">
              https://t.me/{usernameInput || DEFAULT_BOT_USERNAME}?start=m-1_30_2-2_25_1
            </code>
          </div>

          <div className="flex items-center justify-between gap-3 pt-2">
            <button
              type="button"
              onClick={handleReset}
              className="flex items-center gap-1.5 px-3 py-2.5 rounded-xl bg-stone-800 hover:bg-stone-750 text-stone-300 text-xs font-semibold border border-stone-700 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Сбросить</span>
            </button>

            <button
              type="submit"
              className="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-bold text-xs shadow-md shadow-amber-500/20 transition-all active:scale-95"
            >
              {savedSuccess ? (
                <>
                  <Check className="w-4 h-4 text-emerald-950" />
                  <span>Сохранено!</span>
                </>
              ) : (
                <span>Сохранить username</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
