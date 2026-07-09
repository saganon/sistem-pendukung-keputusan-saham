"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

type AppModalProps = {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  className?: string;
  ariaLabel?: string;
};

export function AppModal({
  open,
  onClose,
  children,
  className,
  ariaLabel = "Dialog",
}: AppModalProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!open) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    window.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [open, onClose]);

  if (!mounted || !open) return null;

  return createPortal(
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-label={ariaLabel}
    >
      <div
        className="absolute inset-0 bg-slate-900/45"
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        className={cn(
          "relative z-10 flex max-h-[min(90vh,640px)] w-full max-w-lg flex-col rounded-2xl border border-slate-200 bg-white shadow-lg overflow-hidden",
          className
        )}
      >
        {children}
      </div>
    </div>,
    document.body
  );
}

type AppModalHeaderProps = {
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  onClose: () => void;
};

export function AppModalHeader({
  title,
  subtitle,
  onClose,
}: AppModalHeaderProps) {
  return (
    <div className="flex shrink-0 items-start justify-between gap-3 border-b border-slate-100 px-5 py-4">
      <div className="min-w-0 flex-1">
        <div className="text-sm font-bold text-slate-900 leading-snug break-words whitespace-normal [overflow-wrap:anywhere]">
          {title}
        </div>
        {subtitle ? (
          <div className="text-[12px] text-slate-500 mt-0.5 leading-relaxed break-words whitespace-normal [overflow-wrap:anywhere]">
            {subtitle}
          </div>
        ) : null}
      </div>
      <button
        type="button"
        onClick={onClose}
        className="shrink-0 rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors"
        aria-label="Tutup"
      >
        <X className="size-4" />
      </button>
    </div>
  );
}

export function AppModalBody({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-4",
        className
      )}
    >
      {children}
    </div>
  );
}

export function AppModalFooter({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="shrink-0 border-t border-slate-100 px-5 py-3 flex justify-end">
      {children}
    </div>
  );
}
