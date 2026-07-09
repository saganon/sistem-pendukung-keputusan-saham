"use client";

import {
  createContext,
  useCallback,
  useContext,
  useState,
} from "react";
import { Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  AppModal,
  AppModalBody,
  AppModalFooter,
  AppModalHeader,
} from "@/components/app-modal";
import { getStockInfo } from "@/lib/stock-glossary";
import { cn } from "@/lib/utils";

const WRAP_TEXT =
  "break-words whitespace-normal [overflow-wrap:anywhere] hyphens-auto";

type StockInfoContextValue = {
  openStockInfo: (kode: string) => void;
};

const StockInfoContext = createContext<StockInfoContextValue | null>(null);

function StockInfoModal({
  kode,
  onClose,
}: {
  kode: string;
  onClose: () => void;
}) {
  const info = getStockInfo(kode);
  if (!info) return null;

  return (
    <AppModal
      open
      onClose={onClose}
      ariaLabel={`Info saham ${info.kode}`}
    >
      <AppModalHeader
        title={
          <span className="text-lg font-extrabold">{info.kode}</span>
        }
        subtitle={info.nama}
        onClose={onClose}
      />

      <AppModalBody className="space-y-4">
        <div>
          <h3 className="text-xs font-bold text-slate-700 mb-1.5">
            Apa arti kode {info.kode}?
          </h3>
          <p className={cn("text-[13px] text-slate-600 leading-relaxed", WRAP_TEXT)}>
            {info.artiSingkatan}
          </p>
        </div>
        <div>
          <h3 className="text-xs font-bold text-slate-700 mb-1.5">
            Bidang usaha
          </h3>
          <p className={cn("text-[13px] text-slate-600 leading-relaxed", WRAP_TEXT)}>
            {info.bidangUsaha}
          </p>
        </div>
        <div>
          <h3 className="text-xs font-bold text-slate-700 mb-1.5">
            Tentang perusahaan
          </h3>
          <p className={cn("text-[13px] text-slate-600 leading-relaxed", WRAP_TEXT)}>
            {info.deskripsi}
          </p>
        </div>
      </AppModalBody>

      <AppModalFooter>
        <Button size="sm" onClick={onClose}>
          Mengerti
        </Button>
      </AppModalFooter>
    </AppModal>
  );
}

export function StockInfoProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [activeKode, setActiveKode] = useState<string | null>(null);

  const openStockInfo = useCallback((kode: string) => {
    if (getStockInfo(kode)) setActiveKode(kode);
  }, []);

  const closeStockInfo = useCallback(() => {
    setActiveKode(null);
  }, []);

  return (
    <StockInfoContext.Provider value={{ openStockInfo }}>
      {children}
      {activeKode ? (
        <StockInfoModal kode={activeKode} onClose={closeStockInfo} />
      ) : null}
    </StockInfoContext.Provider>
  );
}

type StockInfoButtonProps = {
  kode: string;
  className?: string;
};

export function StockInfoButton({ kode, className }: StockInfoButtonProps) {
  const ctx = useContext(StockInfoContext);

  if (!getStockInfo(kode)) return null;

  return (
    <button
      type="button"
      onClick={() => ctx?.openStockInfo(kode)}
      className={cn(
        "inline-flex items-center justify-center rounded-full p-0.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors",
        className
      )}
      aria-label={`Info kode saham ${kode}`}
    >
      <Info className="size-3.5" />
    </button>
  );
}

type StockLabelProps = {
  kode: string;
  nama: string;
  showAbbreviation?: boolean;
  showInfo?: boolean;
};

export function StockLabel({
  kode,
  nama,
  showAbbreviation = true,
  showInfo = true,
}: StockLabelProps) {
  const info = getStockInfo(kode);

  return (
    <div className="min-w-0 max-w-[220px] sm:max-w-none">
      <div className="flex items-center gap-1">
        <p className="font-bold text-slate-800 text-sm shrink-0">{kode}</p>
        {showInfo ? <StockInfoButton kode={kode} /> : null}
      </div>
      <p className={cn("text-xs text-slate-400 leading-relaxed", WRAP_TEXT)}>
        {nama}
      </p>
      {showAbbreviation && info ? (
        <p
          className={cn(
            "text-[10px] text-slate-400 mt-0.5 leading-relaxed italic",
            WRAP_TEXT
          )}
        >
          {info.artiSingkatan}
        </p>
      ) : null}
    </div>
  );
}
