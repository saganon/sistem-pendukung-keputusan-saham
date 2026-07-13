"use client";

import { useState } from "react";
import type { DashboardData, Klasifikasi } from "@/lib/types";
import { CRITERIA_FRIENDLY } from "@/lib/glossary";
import { getStockInfo } from "@/lib/stock-glossary";
import { InfoButton, InfoModalProvider } from "@/components/info-modal";
import { SectionHeader } from "@/components/section-header";
import { StockInfoProvider, StockLabel } from "@/components/stock-info";
import { StockReferenceSection } from "@/components/stock-reference";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  ZAxis,
  Label,
} from "recharts";

const formatRupiah = (n: number) => "Rp " + n.toLocaleString("id-ID");
const formatPct = (n: number) => n.toFixed(2) + "%";

const KLASIFIKASI_LABEL: Record<Klasifikasi, string> = {
  Undervalued: "Masih Murah",
  Overvalued: "Mahal",
  "Tidak Valid": "Data Tidak Lengkap",
};

const NAV_ITEMS = [
  { id: "kesimpulan", label: "Kesimpulan" },
  { id: "kode-saham", label: "Kode Saham" },
  { id: "harga-wajar", label: "Harga Wajar" },
  { id: "faktor", label: "Faktor Penting" },
  { id: "peringkat", label: "Peringkat" },
  { id: "pengujian", label: "Pengujian" },
];

function RankBadge({ rank, total }: { rank: number; total: number }) {
  const color =
    rank === 1
      ? "bg-emerald-100 text-emerald-800 border-emerald-200"
      : rank <= 3
        ? "bg-blue-100 text-blue-800 border-blue-200"
        : rank >= total
          ? "bg-red-100 text-red-800 border-red-200"
          : "bg-slate-100 text-slate-700 border-slate-200";
  return (
    <span
      className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold border ${color}`}
    >
      {rank}
    </span>
  );
}

function RankDelta({ rankA, rankB }: { rankA: number; rankB: number }) {
  const diff = rankA - rankB;
  if (diff === 0)
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full">
        → Sama
      </span>
    );
  if (diff > 0)
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
        ↑ Naik {Math.abs(diff)} peringkat
      </span>
    );
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium text-red-600 bg-red-50 px-2 py-0.5 rounded-full">
      ↓ Turun {Math.abs(diff)} peringkat
    </span>
  );
}

function StatusBadge({ klasifikasi }: { klasifikasi: Klasifikasi }) {
  const styles: Record<Klasifikasi, string> = {
    Undervalued: "text-emerald-700 bg-emerald-50 border-emerald-200",
    Overvalued: "text-red-600 bg-red-50 border-red-200",
    "Tidak Valid": "text-slate-500 bg-slate-50 border-slate-200",
  };
  return (
    <span
      className={`inline-flex text-[10px] font-semibold px-2 py-0.5 rounded-full border ${styles[klasifikasi]}`}
    >
      {KLASIFIKASI_LABEL[klasifikasi]}
    </span>
  );
}

const CustomDot = (props: {
  cx?: number;
  cy?: number;
  payload?: { kode: string };
}) => {
  const { cx, cy, payload } = props;
  if (cx == null || cy == null) return null;
  return (
    <g>
      <circle
        cx={cx}
        cy={cy}
        r={7}
        fill="#3b82f6"
        fillOpacity={0.85}
        stroke="#1d4ed8"
        strokeWidth={1.5}
      />
      <text
        x={cx}
        y={cy - 12}
        textAnchor="middle"
        fontSize={10}
        fill="#475569"
        fontWeight={600}
      >
        {payload?.kode}
      </text>
    </g>
  );
};

type DashboardProps = {
  data: DashboardData;
};

export function Dashboard({ data }: DashboardProps) {
  const { stocks, entropyWeights, meta, summary } = data;
  const [activeTab, setActiveTab] = useState<"sep" | "apr">("sep");
  const [tableMode, setTableMode] = useState<"ringkas" | "detail">("ringkas");

  const totalEmiten = stocks.length;
  const chartData = stocks.map((s) => ({
    kode: s.kode,
    "Harga Saat Ini": s.hargaPasar,
    "Harga Wajar": s.grahamNumber,
  }));

  const sortedStocks = [...stocks].sort((a, b) => a.rankTopsis - b.rankTopsis);
  const topStock = sortedStocks[0];
  const undervaluedCount = stocks.filter(
    (s) => s.klasifikasi === "Undervalued"
  ).length;
  const allUndervalued = undervaluedCount === totalEmiten;

  const dominanBobot = summary.dominanBobot;
  const dominanKey = dominanBobot.toLowerCase() as keyof typeof entropyWeights;
  const dominanWeight = entropyWeights[dominanKey] ?? entropyWeights.eps;
  const dominanFriendly = CRITERIA_FRIENDLY[dominanBobot] ?? dominanBobot;

  const scatterData = stocks.map((s) => ({
    kode: s.kode,
    x: s.rankTopsis,
    y:
      activeTab === "sep"
        ? s.rankApr2025vsSep2025
        : s.rankApr2025vsApr2026,
    z: 1,
  }));

  const summaryCards = [
    {
      label: "Saham Dianalisis",
      value: String(totalEmiten),
      sub: "Perusahaan energi terpilih",
      valueColor: "text-slate-800",
    },
    {
      label: "Saham Masih Murah",
      value: String(undervaluedCount),
      sub: allUndervalued
        ? "Semua di bawah harga wajar"
        : `dari ${totalEmiten} saham`,
      valueColor: "text-emerald-600",
    },
    {
      label: "Peringkat Objektif Teratas",
      value: topStock.kode,
      sub: `Peringkat 1 dari ${totalEmiten} saham`,
      valueColor: "text-blue-600",
    },
    {
      label: "Faktor Terpenting",
      value: dominanFriendly,
      sub: `Kontribusi ${(dominanWeight * 100).toFixed(0)}% dalam penilaian`,
      valueColor: "text-violet-600",
    },
  ];

  const criteriaCards = [
    {
      key: "eps",
      infoKey: "eps",
      label: CRITERIA_FRIENDLY.EPS,
      direction: "Semakin tinggi semakin baik",
      directionColor: "text-emerald-600",
      weight: entropyWeights.eps,
      bar: "bg-violet-500",
    },
    {
      key: "der",
      infoKey: "der",
      label: CRITERIA_FRIENDLY.DER,
      direction: "Semakin rendah semakin baik",
      directionColor: "text-amber-700",
      weight: entropyWeights.der,
      bar: "bg-amber-400",
    },
    {
      key: "roa",
      infoKey: "roa",
      label: CRITERIA_FRIENDLY.ROA,
      direction: "Semakin tinggi semakin baik",
      directionColor: "text-emerald-600",
      weight: entropyWeights.roa,
      bar: "bg-blue-500",
    },
    {
      key: "pbv",
      infoKey: "pbv",
      label: CRITERIA_FRIENDLY.PBV,
      direction: "Semakin rendah semakin baik",
      directionColor: "text-amber-700",
      weight: entropyWeights.pbv,
      bar: "bg-slate-400",
    },
  ];

  return (
    <InfoModalProvider>
      <StockInfoProvider>
        <main
          className="min-h-screen bg-[#f8fafc]"
          style={{ fontFamily: "'Inter', 'system-ui', sans-serif" }}
        >
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-8 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shrink-0">
              <span className="text-white text-xs font-bold">RS</span>
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h1 className="text-sm sm:text-base font-bold text-slate-900 leading-snug tracking-tight">
                  Peringkat Objektif Saham Energi
                </h1>
                <InfoButton infoKey="overview" />
              </div>
              <p className="text-[11px] text-slate-400 mt-0.5 tracking-wide">
                Analisis {totalEmiten} perusahaan energi terpilih · Laporan
                keuangan {meta.tahunLaporan}
              </p>
            </div>
          </div>
          <div className="text-right shrink-0 hidden sm:block">
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Harga saham per {meta.tanggalHarga}
            </p>
            <p className="text-[11px] font-semibold text-slate-600">
              Sumber: {meta.sumberData}
            </p>
          </div>
        </div>

        <nav className="border-t border-slate-100 bg-slate-50/80">
          <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-8 flex gap-1 overflow-x-auto py-2">
            {NAV_ITEMS.map((item) => (
              <a
                key={item.id}
                href={`#${item.id}`}
                className="shrink-0 text-[11px] font-semibold text-slate-500 hover:text-blue-600 hover:bg-blue-50 px-3 py-1.5 rounded-lg transition-colors"
              >
                {item.label}
              </a>
            ))}
          </div>
        </nav>
      </header>

      <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-8 py-8 space-y-7">
        <section id="kesimpulan" className="scroll-mt-28">
          <div className="rounded-2xl border border-blue-100 bg-gradient-to-br from-blue-50 to-white px-5 py-5 sm:px-6">
            <p className="text-[11px] font-bold text-blue-600 uppercase tracking-widest mb-2">
              Kesimpulan Analisis
            </p>
            <p className="text-sm text-slate-700 leading-relaxed">
              Berdasarkan analisis sistem, saham{" "}
              <strong className="text-slate-900">{topStock.kode}</strong> (
              {topStock.nama}) menduduki{" "}
              <strong className="text-slate-900">peringkat teratas</strong> dari{" "}
              {totalEmiten} emiten energi yang dibandingkan.
              {allUndervalued ? (
                <>
                  {" "}
                  Seluruh saham dalam daftar ini dinilai masih{" "}
                  <strong className="text-emerald-700">di bawah harga wajar</strong>
                  .
                </>
              ) : (
                <>
                  {" "}
                  Sebanyak {undervaluedCount} saham dinilai masih di bawah harga
                  wajar.
                </>
              )}
            </p>
            <p className="text-[12px] text-amber-700 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2 mt-3 leading-relaxed">
              ⚠️ Hasil ini adalah alat bantu analisis, bukan saran untuk membeli
              atau menjual saham. Selalu lakukan riset sendiri sebelum
              berinvestasi.
            </p>
          </div>
        </section>

        <StockReferenceSection />

        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {summaryCards.map((c) => (
            <Card
              key={c.label}
              className="border-slate-200 bg-white shadow-sm hover:shadow-md transition-shadow"
            >
              <CardContent className="p-5 flex flex-col justify-between h-full min-h-[120px]">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-3">
                  {c.label}
                </p>
                <div>
                  <p
                    className={`text-2xl sm:text-3xl font-extrabold leading-none tracking-tight ${c.valueColor}`}
                  >
                    {c.value}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-2 font-medium leading-relaxed">
                    {c.sub}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </section>

        <section id="harga-wajar" className="scroll-mt-28">
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-1 px-6 pt-6">
              <SectionHeader
                title="Apakah Harganya Masih Murah?"
                subtitle="Batang hijau = harga saat ini. Batang biru = perkiraan harga wajar. Jika hijau lebih pendek, saham dinilai masih murah."
                infoKey="graham"
              />
            </CardHeader>
            <CardContent className="px-2 sm:px-4 pb-6 pt-2">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart
                  data={chartData}
                  margin={{ top: 16, right: 16, left: 0, bottom: 0 }}
                  barGap={4}
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#e2e8f0"
                    vertical={false}
                  />
                  <XAxis
                    dataKey="kode"
                    tick={{ fontSize: 12, fill: "#64748b", fontWeight: 600 }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fontSize: 10, fill: "#94a3b8" }}
                    tickFormatter={(v) =>
                      v >= 1000 ? (v / 1000).toFixed(0) + "k" : String(v)
                    }
                    axisLine={false}
                    tickLine={false}
                    width={38}
                  />
                  <Tooltip
                    formatter={(value, name) => [
                      formatRupiah(Number(value ?? 0)),
                      String(name),
                    ]}
                    labelFormatter={(label) => {
                      const info = getStockInfo(String(label));
                      return info
                        ? `${label} — ${info.nama}`
                        : String(label);
                    }}
                    contentStyle={{
                      fontSize: 12,
                      borderRadius: 10,
                      border: "1px solid #e2e8f0",
                      boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                    }}
                    cursor={{ fill: "#f1f5f9" }}
                  />
                  <Legend
                    wrapperStyle={{
                      fontSize: 12,
                      paddingTop: 16,
                      color: "#475569",
                    }}
                  />
                  <Bar
                    dataKey="Harga Wajar"
                    fill="#1e3a5f"
                    radius={[5, 5, 0, 0]}
                    maxBarSize={40}
                  />
                  <Bar
                    dataKey="Harga Saat Ini"
                    fill="#10b981"
                    radius={[5, 5, 0, 0]}
                    maxBarSize={40}
                  />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </section>

        <section id="faktor" className="scroll-mt-28">
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-2 px-6 pt-6">
              <SectionHeader
                title="Faktor Apa yang Paling Berpengaruh?"
                subtitle="Sistem menilai seberapa penting setiap faktor keuangan dalam membedakan saham yang baik dan kurang baik."
                infoKey="entropy"
              />
            </CardHeader>
            <CardContent className="px-6 pb-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                {criteriaCards.map((c) => (
                  <div
                    key={c.key}
                    className="rounded-xl border border-slate-100 bg-slate-50 p-4"
                  >
                    <div className="flex items-center justify-between mb-1.5 gap-2">
                      <span className="text-sm font-extrabold text-slate-800 tracking-tight leading-snug">
                        {c.label}
                      </span>
                      <InfoButton infoKey={c.infoKey} />
                    </div>
                    <p
                      className={`text-[11px] font-medium mb-3 ${c.directionColor}`}
                    >
                      {c.direction}
                    </p>
                    <div className="w-full bg-slate-200 rounded-full h-1.5 mb-2">
                      <div
                        className={`${c.bar} h-1.5 rounded-full transition-all`}
                        style={{ width: `${c.weight * 100}%` }}
                      />
                    </div>
                    <p className="text-right text-sm font-extrabold text-slate-700">
                      {formatPct(c.weight * 100)}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        <section id="peringkat" className="scroll-mt-28">
          <Card className="border-slate-200">
            <CardHeader className="pb-3 px-6 pt-6">
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                <SectionHeader
                  title="Peringkat Objektif Saham"
                  subtitle="Saham diurutkan dari yang paling baik secara fundamental (peringkat 1) hingga yang paling rendah."
                  infoKey="topsis"
                />
                <div className="flex gap-1 shrink-0 bg-slate-100 rounded-lg p-1">
                  {(["ringkas", "detail"] as const).map((mode) => (
                    <button
                      key={mode}
                      type="button"
                      onClick={() => setTableMode(mode)}
                      className={`text-[11px] px-3 py-1.5 rounded-md font-semibold transition-colors capitalize ${
                        tableMode === mode
                          ? "bg-white text-slate-800 shadow-sm"
                          : "text-slate-500 hover:text-slate-700"
                      }`}
                    >
                      {mode}
                    </button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-5 pt-0 overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-slate-50 hover:bg-slate-50">
                    <TableHead className="text-xs font-semibold text-slate-600 w-12">
                      Peringkat
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600">
                      Saham
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      Harga Saat Ini
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-center">
                      Status Harga
                    </TableHead>
                    {tableMode === "detail" ? (
                      <>
                        <TableHead className="text-xs font-semibold text-slate-600 text-right">
                          Harga Wajar
                        </TableHead>
                        <TableHead className="text-xs font-semibold text-slate-600 text-right">
                          {CRITERIA_FRIENDLY.EPS}
                        </TableHead>
                        <TableHead className="text-xs font-semibold text-slate-600 text-right">
                          {CRITERIA_FRIENDLY.ROA}
                        </TableHead>
                        <TableHead className="text-xs font-semibold text-slate-600 text-right">
                          {CRITERIA_FRIENDLY.DER}
                        </TableHead>
                        <TableHead className="text-xs font-semibold text-slate-600 text-right">
                          Skor Penilaian
                        </TableHead>
                      </>
                    ) : null}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedStocks.map((s) => (
                    <TableRow
                      key={s.kode}
                      className="hover:bg-slate-50/80 transition-colors"
                    >
                      <TableCell>
                        <RankBadge rank={s.rankTopsis} total={totalEmiten} />
                      </TableCell>
                      <TableCell className="whitespace-normal align-top min-w-[160px]">
                        <StockLabel
                          kode={s.kode}
                          nama={s.nama}
                          showAbbreviation={false}
                        />
                      </TableCell>
                      <TableCell className="text-right text-sm text-slate-700">
                        {formatRupiah(s.hargaPasar)}
                      </TableCell>
                      <TableCell className="text-center">
                        <StatusBadge klasifikasi={s.klasifikasi} />
                      </TableCell>
                      {tableMode === "detail" ? (
                        <>
                          <TableCell className="text-right text-sm text-emerald-700 font-medium">
                            {formatRupiah(s.grahamNumber)}
                          </TableCell>
                          <TableCell className="text-right text-sm text-slate-700">
                            {formatRupiah(s.eps)}
                          </TableCell>
                          <TableCell className="text-right text-sm text-slate-700">
                            {formatPct(s.roa)}
                          </TableCell>
                          <TableCell className="text-right text-sm text-slate-700">
                            {s.der.toFixed(2)}x
                          </TableCell>
                          <TableCell className="text-right">
                            <span className="text-sm font-bold text-slate-800">
                              {s.skorTopsis.toFixed(2)}
                            </span>
                          </TableCell>
                        </>
                      ) : null}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </section>

        <section id="pengujian" className="scroll-mt-28">
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-2 px-6 pt-6">
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                <SectionHeader
                  title="Apakah Peringkat Analisis Terbukti Benar?"
                  subtitle="Sistem membandingkan peringkat analisis dengan kenaikan harga saham yang benar-benar terjadi setelahnya."
                  infoKey="backtesting"
                />
                <div className="flex gap-2 shrink-0">
                  {(["sep", "apr"] as const).map((tab) => (
                    <button
                      key={tab}
                      type="button"
                      onClick={() => setActiveTab(tab)}
                      className={`text-[11px] px-3 py-1.5 rounded-lg font-semibold transition-colors whitespace-nowrap ${
                        activeTab === tab
                          ? "bg-blue-600 text-white shadow-sm"
                          : "bg-slate-100 text-slate-500 hover:bg-slate-200"
                      }`}
                    >
                      {tab === "sep" ? "Apr → Sep 2025" : "Apr 2025 → Apr 2026"}
                    </button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent className="px-6 pb-6 space-y-6">
              <div className="bg-slate-50 rounded-xl p-4">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">
                  Perbandingan Peringkat
                </p>
                <p className="text-[11px] text-slate-400 mb-4">
                  Sumbu horizontal = peringkat analisis sistem · Sumbu vertikal =
                  peringkat kenaikan harga nyata
                </p>
                <ResponsiveContainer width="100%" height={260}>
                  <ScatterChart
                    margin={{ top: 20, right: 30, left: 0, bottom: 20 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis
                      type="number"
                      dataKey="x"
                      domain={[0.5, totalEmiten + 0.5]}
                      ticks={Array.from({ length: totalEmiten }, (_, i) => i + 1)}
                      tick={{ fontSize: 11, fill: "#64748b" }}
                      axisLine={false}
                      tickLine={false}
                    >
                      <Label
                        value="Peringkat Analisis Sistem"
                        offset={-10}
                        position="insideBottom"
                        style={{
                          fontSize: 11,
                          fill: "#94a3b8",
                          fontWeight: 600,
                        }}
                      />
                    </XAxis>
                    <YAxis
                      type="number"
                      dataKey="y"
                      domain={[0.5, totalEmiten + 0.5]}
                      ticks={Array.from({ length: totalEmiten }, (_, i) => i + 1)}
                      tick={{ fontSize: 11, fill: "#64748b" }}
                      axisLine={false}
                      tickLine={false}
                      width={28}
                    >
                      <Label
                        value="Peringkat Kenaikan Harga"
                        angle={-90}
                        position="insideLeft"
                        style={{
                          fontSize: 11,
                          fill: "#94a3b8",
                          fontWeight: 600,
                        }}
                      />
                    </YAxis>
                    <ZAxis dataKey="z" range={[60, 60]} />
                    <Tooltip
                      cursor={{ strokeDasharray: "3 3" }}
                      content={({ payload }) => {
                        if (!payload?.length) return null;
                        const d = payload[0].payload;
                        const info = getStockInfo(d.kode);
                        return (
                          <div className="bg-white border border-slate-200 rounded-lg px-3 py-2 shadow-lg text-xs max-w-[220px]">
                            <p className="font-bold text-slate-800">{d.kode}</p>
                            {info ? (
                              <p className="text-slate-400 text-[10px] leading-snug mb-1.5">
                                {info.nama}
                              </p>
                            ) : null}
                            <p className="text-slate-500">
                              Peringkat analisis:{" "}
                              <span className="font-semibold text-blue-600">
                                {d.x}
                              </span>
                            </p>
                            <p className="text-slate-500">
                              Peringkat kenaikan harga:{" "}
                              <span className="font-semibold text-emerald-600">
                                {d.y}
                              </span>
                            </p>
                          </div>
                        );
                      }}
                    />
                    <Scatter data={scatterData} shape={<CustomDot />} />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>

              <div className="overflow-x-auto">
                <Table className="min-w-[480px]">
                  <TableHeader>
                    <TableRow className="bg-slate-50 hover:bg-slate-50 border-b border-slate-200">
                      {[
                        "Saham",
                        "Peringkat Analisis",
                        "Peringkat Kenaikan Harga",
                        "Perubahan",
                      ].map((h, i) => (
                        <TableHead
                          key={h}
                          className={`text-[11px] font-bold text-slate-500 uppercase tracking-widest py-3 ${i > 0 ? "text-center" : "pl-4"}`}
                        >
                          {h}
                        </TableHead>
                      ))}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {sortedStocks.map((s) => {
                      const rankAktual =
                        activeTab === "sep"
                          ? s.rankApr2025vsSep2025
                          : s.rankApr2025vsApr2026;
                      return (
                        <TableRow
                          key={s.kode}
                          className="hover:bg-slate-50/80 border-b border-slate-100"
                        >
                          <TableCell className="pl-4 py-3 whitespace-normal align-top min-w-[160px]">
                            <StockLabel
                              kode={s.kode}
                              nama={s.nama}
                              showAbbreviation={false}
                            />
                          </TableCell>
                          <TableCell className="text-center py-3">
                            <RankBadge rank={s.rankTopsis} total={totalEmiten} />
                          </TableCell>
                          <TableCell className="text-center py-3">
                            <RankBadge rank={rankAktual} total={totalEmiten} />
                          </TableCell>
                          <TableCell className="text-center py-3">
                            <RankDelta rankA={s.rankTopsis} rankB={rankAktual} />
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>

              <div className="rounded-xl bg-amber-50 border border-amber-100 px-5 py-4">
                <p className="text-[11px] font-bold text-amber-700 uppercase tracking-widest mb-1">
                  Apa artinya untuk Anda?
                </p>
                <p className="text-[12px] text-amber-800 leading-relaxed">
                  Dari data yang sistem uji, peringkat analisis fundamental{" "}
                  <strong>belum selalu sama</strong> dengan kenaikan harga aktual.
                  Artinya, harga saham juga dipengaruhi kondisi ekonomi global,
                  harga komoditas, dan berita pasar — bukan hanya angka keuangan
                  perusahaan. Gunakan hasil ini sebagai salah satu referensi,
                  bukan satu-satunya alasan untuk berinvestasi.
                </p>
              </div>
            </CardContent>
          </Card>
        </section>

        <footer className="text-center py-8 border-t border-slate-200 space-y-1">
          <p className="text-[11px] text-slate-400 tracking-wide">
            Peringkat Objektif Saham Energi · 2026
          </p>
        </footer>
      </div>
    </main>
      </StockInfoProvider>
    </InfoModalProvider>
  );
}
