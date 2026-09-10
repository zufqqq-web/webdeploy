import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { CheckCircle2, Info, AlertCircle, X } from 'lucide-react';
import { useCart } from '../context/CartContext';

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useCart();

  return (
    <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-2 w-full max-w-sm px-4 pointer-events-none">
      <AnimatePresence>
        {toasts.map((toast) => {
          return (
            <motion.div
              key={toast.id}
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9, y: -10 }}
              transition={{ duration: 0.2 }}
              className="pointer-events-auto flex items-center justify-between gap-3 px-4 py-3 rounded-2xl bg-stone-900/95 backdrop-blur-md text-white border border-stone-750 shadow-2xl shadow-black/50 text-xs font-semibold w-full"
            >
              <div className="flex items-center gap-2.5 min-w-0">
                {toast.type === 'success' && (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                )}
                {toast.type === 'info' && (
                  <Info className="w-4 h-4 text-sky-400 flex-shrink-0" />
                )}
                {toast.type === 'warning' && (
                  <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                )}
                <span className="truncate">{toast.message}</span>
              </div>

              <button
                type="button"
                onClick={() => removeToast(toast.id)}
                className="text-stone-400 hover:text-white p-0.5"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
};
