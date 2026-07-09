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
import { INFO_CONTENT } from "@/lib/glossary";
import { cn } from "@/lib/utils";

type InfoModalContextValue = {
  openInfo: (infoKey: string) => void;
};

const InfoModalContext = createContext<InfoModalContextValue | null>(null);

function InfoModalContent({
  infoKey,
  onClose,
}: {
  infoKey: string;
  onClose: () => void;
}) {
  const content = INFO_CONTENT[infoKey];
  if (!content) return null;

  return (
    <AppModal open onClose={onClose} ariaLabel={content.title}>
      <AppModalHeader title={content.title} onClose={onClose} />

      <AppModalBody className="space-y-4">
        {content.sections.map((section) => (
          <div key={section.heading}>
            <h3 className="text-xs font-bold text-slate-700 mb-1.5">
              {section.heading}
            </h3>
            {section.body ? (
              <p className="text-[13px] text-slate-600 leading-relaxed break-words whitespace-normal [overflow-wrap:anywhere]">
                {section.body}
              </p>
            ) : null}
            {section.items ? (
              <ul className="mt-1 space-y-1">
                {section.items.map((item) => (
                  <li
                    key={item}
                    className="text-[13px] text-slate-600 leading-relaxed flex gap-2"
                  >
                    <span className="text-blue-500 shrink-0">•</span>
                    <span className="break-words whitespace-normal [overflow-wrap:anywhere]">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            ) : null}
            {section.technical ? (
              <pre className="mt-2 rounded-lg bg-slate-50 border border-slate-100 px-3 py-2.5 text-[11px] text-slate-500 leading-relaxed whitespace-pre-wrap break-words font-sans">
                {section.technical}
              </pre>
            ) : null}
          </div>
        ))}
      </AppModalBody>

      <AppModalFooter>
        <Button size="sm" onClick={onClose}>
          Mengerti
        </Button>
      </AppModalFooter>
    </AppModal>
  );
}

export function InfoModalProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [activeKey, setActiveKey] = useState<string | null>(null);

  const openInfo = useCallback((infoKey: string) => {
    if (INFO_CONTENT[infoKey]) setActiveKey(infoKey);
  }, []);

  const closeInfo = useCallback(() => {
    setActiveKey(null);
  }, []);

  return (
    <InfoModalContext.Provider value={{ openInfo }}>
      {children}
      {activeKey ? (
        <InfoModalContent infoKey={activeKey} onClose={closeInfo} />
      ) : null}
    </InfoModalContext.Provider>
  );
}

type InfoButtonProps = {
  infoKey: string;
  label?: string;
  className?: string;
};

export function InfoButton({
  infoKey,
  label = "Info",
  className,
}: InfoButtonProps) {
  const ctx = useContext(InfoModalContext);

  if (!INFO_CONTENT[infoKey]) return null;

  return (
    <button
      type="button"
      onClick={() => ctx?.openInfo(infoKey)}
      className={cn(
        "inline-flex items-center gap-1 rounded-full border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-500 hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50 transition-colors",
        className
      )}
      aria-label={label}
    >
      <Info className="size-3" />
      <span>Info</span>
    </button>
  );
}
