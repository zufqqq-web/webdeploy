import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Rocket, CheckCircle2, ExternalLink } from 'lucide-react';

interface OrderLoadingModalProps {
  isOpen: boolean;
  deepLinkUrl: string;
  onManualOpen: () => void;
  onClose: () => void;
}

export const OrderLoadingModal: React.FC<OrderLoadingModalProps> = ({
  isOpen,
  deepLinkUrl,
  onManualOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/85 backdrop-blur-md"
        />

        {/* Card */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 10 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 10 }}
          className="relative w-full max-w-sm bg-stone-900 border border-amber-500/40 rounded-3xl p-6 shadow-2xl text-center space-y-4 z-10"
        >
          {/* Animated Rocket Icon */}
          <div className="w-16 h-16 mx-auto rounded-3xl bg-gradient-to-tr from-amber-500 to-amber-400 text-stone-950 flex items-center justify-center shadow-xl shadow-amber-500/30 border border-amber-300">
            <motion.div
              animate={{ y: [-2, -8, -2], rotate: [-2, 2, -2] }}
              transition={{ repeat: Infinity, duration: 1.6, ease: 'easeInOut' }}
            >
              <Rocket className="w-8 h-8" />
            </motion.div>
          </div>

          <div className="space-y-1">
            <h3 className="text-xl font-extrabold text-white">
              🚀 Открываем Telegram...
            </h3>
            <p className="text-xs text-stone-400">
              Формируем заказ и передаем боту параметры корзины
            </p>
          </div>

          {/* Generated deep link details */}
          <div className="p-3 bg-stone-950 rounded-2xl border border-stone-800 text-left space-y-1">
            <span className="text-[10px] text-stone-500 uppercase tracking-wider font-bold">
              Параметры ссылки:
            </span>
            <p className="text-xs font-mono text-amber-300 break-all leading-relaxed">
              {deepLinkUrl}
            </p>
          </div>

          {/* Manual open fallback button */}
          <div className="pt-2 space-y-2">
            <button
              id="manual-open-telegram-btn"
              onClick={onManualOpen}
              className="w-full py-3 px-4 rounded-xl bg-amber-500 hover:bg-amber-400 text-stone-950 font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-amber-500/20 active:scale-95 transition-all"
            >
              <ExternalLink className="w-4 h-4" />
              <span>Перейти в чат с ботом</span>
            </button>

            <button
              onClick={onClose}
              className="text-xs text-stone-400 hover:text-stone-200 py-1 transition-colors"
            >
              Вернуться в приложение
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
