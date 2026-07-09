"use client";

import { STOCK_GLOSSARY } from "@/lib/stock-glossary";
import { StockInfoButton } from "@/components/stock-info";
import { SectionHeader } from "@/components/section-header";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function StockReferenceSection() {
  const stocks = Object.values(STOCK_GLOSSARY);

  return (
    <section id="kode-saham" className="scroll-mt-28">
      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="pb-2 px-6 pt-6">
          <SectionHeader
            title="Mengenal Kode Saham"
            subtitle="Kode 4 huruf (misalnya ADRO, PGAS) adalah singkatan resmi perusahaan di Bursa Efek Indonesia. Klik ikon info untuk penjelasan lengkap."
            infoKey="kode-saham"
          />
        </CardHeader>
        <CardContent className="px-6 pb-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {stocks.map((stock) => (
              <div
                key={stock.kode}
                className="rounded-xl border border-slate-100 bg-slate-50 p-4 flex flex-col gap-2"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-base font-extrabold text-slate-800 tracking-tight">
                    {stock.kode}
                  </span>
                  <StockInfoButton kode={stock.kode} />
                </div>
                <p className="text-[12px] font-semibold text-slate-700 leading-snug break-words whitespace-normal [overflow-wrap:anywhere]">
                  {stock.nama}
                </p>
                <p className="text-[11px] text-slate-500 leading-relaxed break-words whitespace-normal [overflow-wrap:anywhere]">
                  <span className="font-semibold text-slate-600">
                    Arti kode:{" "}
                  </span>
                  {stock.artiSingkatan}
                </p>
                <span className="inline-flex self-start text-[10px] font-semibold text-blue-700 bg-blue-50 border border-blue-100 px-2 py-0.5 rounded-full">
                  {stock.bidangUsaha}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </section>
  );
}
