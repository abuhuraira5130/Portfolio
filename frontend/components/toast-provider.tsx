"use client";

import React, { createContext, useContext, useState, useCallback } from "react";

interface Toast {
  msg: string;
  type: "success" | "error" | "info";
}

interface ToastContextType {
  showToast: (msg: string, type?: "success" | "error" | "info") => void;
  addToast: (msg: string, type?: "success" | "error" | "info") => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toast, setToast] = useState<Toast | null>(null);

  const showToast = useCallback((msg: string, type: "success" | "error" | "info" = "info") => {
    setToast({ msg, type });

    setTimeout(() => {
      setToast(null);
    }, 3000);
  }, []);

  const addToast: ToastContextType["addToast"] = showToast;

  return (
    <ToastContext.Provider value={{ showToast, addToast }}>
      {children}

      {/* Simple Toast UI */}
      {toast && (
        <div
          className={
            "fixed bottom-5 right-5 px-4 py-2 rounded text-white shadow-lg transition-all duration-300 " +
            (toast.type === "success" ? "bg-green-600 " : "") +
            (toast.type === "error" ? "bg-red-600 " : "") +
            (toast.type === "info" ? "bg-blue-600 " : "")
          }
        >
          {toast.msg}
        </div>
      )}
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used inside ToastProvider");
  }
  return context;
}
