"use client";

import { InfoButton } from "@/components/info-modal";

type SectionHeaderProps = {
  title: string;
  subtitle?: string;
  infoKey?: string;
};

export function SectionHeader({ title, subtitle, infoKey }: SectionHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-3">
      <div>
        <div className="flex items-center gap-2 flex-wrap">
          <h2 className="text-sm font-bold text-slate-800 tracking-tight">
            {title}
          </h2>
          {infoKey ? <InfoButton infoKey={infoKey} /> : null}
        </div>
        {subtitle ? (
          <p className="text-[12px] text-slate-500 mt-1 leading-relaxed">
            {subtitle}
          </p>
        ) : null}
      </div>
    </div>
  );
}
