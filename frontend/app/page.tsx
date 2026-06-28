"use client";

import { useState } from "react";
import { STOCKS, ENTROPY_WEIGHTS, META } from "@/lib/data";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
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

function RankBadge({ rank, total = 7 }: { rank: number; total?: number }) {
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
  if (diff < 0)
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
        ↑ +{Math.abs(diff)} posisi
      </span>
    );
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium text-red-600 bg-red-50 px-2 py-0.5 rounded-full">
      ↓ −{Math.abs(diff)} posisi
    </span>
  );
}

const chartData = STOCKS.map((s) => ({
  kode: s.kode,
  "Harga Pasar": s.hargaPasar,
  "Graham Number": s.grahamNumber,
}));

// Custom dot untuk scatter — tampilkan label kode saham
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  return (
    <g>
      <circle cx={cx} cy={cy} r={7} fill="#3b82f6" fillOpacity={0.85} stroke="#1d4ed8" strokeWidth={1.5} />
      <text x={cx} y={cy - 12} textAnchor="middle" fontSize={10} fill="#475569" fontWeight={600}>
        {payload.kode}
      </text>
    </g>
  );
};

export default function Home() {
  const [activeTab, setActiveTab] = useState<"sep" | "apr">("sep");

  const topStock = [...STOCKS].sort((a, b) => a.rankTopsis - b.rankTopsis)[0];
  const undervaluedCount = STOCKS.filter((s) => s.klasifikasi === "Undervalued").length;

  const scatterData = STOCKS.map((s) => ({
    kode: s.kode,
    x: s.rankTopsis,
    y: activeTab === "sep" ? s.rankApr2025vsSep2025 : s.rankApr2025vsApr2026,
    z: 1,
  }));

  const summaryCards = [
    {
      label: "Total Emiten",
      value: String(STOCKS.length),
      sub: "Sektor energi LQ45",
      valueColor: "text-slate-800",
    },
    {
      label: "Lolos Graham",
      value: String(undervaluedCount),
      sub: "Semua undervalued",
      valueColor: "text-emerald-600",
    },
    {
      label: "Rank #1 TOPSIS",
      value: topStock.kode,
      sub: `Skor ${topStock.skorTopsis.toFixed(2)}`,
      valueColor: "text-blue-600",
    },
    {
      label: "Bobot Dominan",
      value: "EPS",
      sub: `Entropy ${(ENTROPY_WEIGHTS.eps * 100).toFixed(0)}%`,
      valueColor: "text-violet-600",
    },
  ];

  return (
    <main className="min-h-screen bg-[#f8fafc]" style={{ fontFamily: "'Inter', 'system-ui', sans-serif" }}>

      {/* ── HEADER ── */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-8 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shrink-0">
              <span className="text-white text-xs font-bold">SPK</span>
            </div>
            <div>
              <h1 className="text-sm sm:text-base font-bold text-slate-900 leading-snug tracking-tight">
                Sistem Pendukung Keputusan Investasi Saham
              </h1>
              <p className="text-[11px] text-slate-400 mt-0.5 tracking-wide">
                Graham Number · Entropy · TOPSIS — Sektor Energi LQ45
              </p>
            </div>
          </div>
          <div className="text-right shrink-0 hidden sm:block">
            <p className="text-[11px] text-slate-400 leading-relaxed">Laporan Keuangan Tahunan {META.tahunLaporan}</p>
            <p className="text-[11px] font-semibold text-slate-600">Harga per {META.tanggalHarga}</p>
          </div>
        </div>
      </header>

      <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-8 py-8 space-y-7">

        {/* ── SUMMARY CARDS ── */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {summaryCards.map((c) => (
            <Card key={c.label} className="border-slate-200 bg-white shadow-sm hover:shadow-md transition-shadow">
              <CardContent className="p-5 flex flex-col justify-between h-full min-h-[120px]">
                <div className="flex items-center justify-between mb-3">
                  <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest">
                    {c.label}
                  </p>
                  <span className="text-base">{c.icon}</span>
                </div>
                <div>
                  <p className={`text-3xl font-extrabold leading-none tracking-tight ${c.valueColor}`}>
                    {c.value}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-2 font-medium">{c.sub}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </section>

        {/* ── GRAHAM CHART ── */}
        <section>
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-1 px-6 pt-6">
              <CardTitle className="text-sm font-bold text-slate-800 tracking-tight">
                Valuasi Graham Number vs Harga Pasar
              </CardTitle>
              <p className="text-[12px] text-slate-500 mt-1">
                Seluruh emiten berada di bawah Graham Number —{" "}
                <span className="text-emerald-600 font-semibold">semua terklasifikasi Undervalued</span>
              </p>
            </CardHeader>
            <CardContent className="px-2 sm:px-4 pb-6 pt-2">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={chartData} margin={{ top: 16, right: 16, left: 0, bottom: 0 }} barGap={4}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                  <XAxis dataKey="kode" tick={{ fontSize: 12, fill: "#64748b", fontWeight: 600 }} axisLine={false} tickLine={false} />
                  <YAxis
                    tick={{ fontSize: 10, fill: "#94a3b8" }}
                    tickFormatter={(v) => (v >= 1000 ? (v / 1000).toFixed(0) + "k" : v)}
                    axisLine={false}
                    tickLine={false}
                    width={38}
                  />
                  <Tooltip
                    formatter={(value: number, name: string) => [formatRupiah(value), name]}
                    contentStyle={{ fontSize: 12, borderRadius: 10, border: "1px solid #e2e8f0", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}
                    cursor={{ fill: "#f1f5f9" }}
                  />
                  <Legend wrapperStyle={{ fontSize: 12, paddingTop: 16, color: "#475569" }} />
                  <Bar dataKey="Graham Number" fill="#1e3a5f" radius={[5, 5, 0, 0]} maxBarSize={40} />
                  <Bar dataKey="Harga Pasar" fill="#10b981" radius={[5, 5, 0, 0]} maxBarSize={40} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </section>

        {/* ── ENTROPY WEIGHTS ── */}
        <section>
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-2 px-6 pt-6">
              <CardTitle className="text-sm font-bold text-slate-800 tracking-tight">
                Bobot Kriteria — Metode Entropy
              </CardTitle>
              <p className="text-[12px] text-slate-500 mt-1">
                Bobot ditentukan secara objektif berdasarkan variasi data, tanpa preferensi subjektif
              </p>
            </CardHeader>
            <CardContent className="px-6 pb-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { key: "EPS", label: "Earnings Per Share", type: "Benefit", weight: ENTROPY_WEIGHTS.eps, bar: "bg-violet-500" },
                  { key: "DER", label: "Debt to Equity Ratio", type: "Cost", weight: ENTROPY_WEIGHTS.der, bar: "bg-amber-400" },
                  { key: "ROA", label: "Return on Assets", type: "Benefit", weight: ENTROPY_WEIGHTS.roa, bar: "bg-blue-500" },
                  { key: "PBV", label: "Price to Book Value", type: "Cost", weight: ENTROPY_WEIGHTS.pbv, bar: "bg-slate-300" },
                ].map((c) => (
                  <div key={c.key} className="rounded-xl border border-slate-100 bg-slate-50 p-4">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-sm font-extrabold text-slate-800 tracking-tight">{c.key}</span>
                      <Badge
                        variant="outline"
                        className={
                          c.type === "Benefit"
                            ? "text-emerald-700 border-emerald-200 bg-emerald-50 text-[10px] px-1.5 font-semibold"
                            : "text-red-600 border-red-200 bg-red-50 text-[10px] px-1.5 font-semibold"
                        }
                      >
                        {c.type}
                      </Badge>
                    </div>
                    <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">{c.label}</p>
                    <div className="w-full bg-slate-200 rounded-full h-1.5 mb-2">
                      <div className={`${c.bar} h-1.5 rounded-full transition-all`} style={{ width: `${c.weight * 100}%` }} />
                    </div>
                    <p className="text-right text-sm font-extrabold text-slate-700">{formatPct(c.weight * 100)}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        {/* ── TOPSIS TABLE ── */}
        <section>
          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold text-slate-800">
                Hasil Peringkat — Metode TOPSIS
              </CardTitle>
              <p className="text-xs text-slate-500">
                Diurutkan berdasarkan skor TOPSIS · Semakin tinggi skor →
                semakin dekat ke solusi ideal positif
              </p>
            </CardHeader>
            <CardContent className="p-5">
              <Table>
                <TableHeader>
                  <TableRow className="bg-slate-50 hover:bg-slate-50">
                    <TableHead className="text-xs font-semibold text-slate-600 w-12">
                      Rank
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600">
                      Emiten
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      Harga Pasar
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      Graham Number
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      EPS
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      ROA
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      DER
                    </TableHead>
                    <TableHead className="text-xs font-semibold text-slate-600 text-right">
                      Skor TOPSIS
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {[...STOCKS]
                    .sort((a, b) => a.rankTopsis - b.rankTopsis)
                    .map((s) => (
                      <TableRow
                        key={s.kode}
                        className="hover:bg-slate-50/80 transition-colors"
                      >
                        <TableCell>
                          <RankBadge rank={s.rankTopsis} />
                        </TableCell>
                        <TableCell>
                          <p className="font-bold text-slate-800 text-sm">
                            {s.kode}
                          </p>
                          <p className="text-xs text-slate-400 leading-tight">
                            {s.nama}
                          </p>
                        </TableCell>
                        <TableCell className="text-right text-sm text-slate-700">
                          {formatRupiah(s.hargaPasar)}
                        </TableCell>
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
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </section>


        {/* ── BACKTESTING ── */}
        <section>
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-2 px-6 pt-6">
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                <div>
                  <CardTitle className="text-sm font-bold text-slate-800 tracking-tight">
                    Backtesting — Perbandingan Rank TOPSIS vs Return Aktual
                  </CardTitle>
                  <p className="text-[12px] text-slate-500 mt-1">
                    Distribusi titik yang tersebar mengindikasikan tidak terdapat pola korelasi antara peringkat fundamental dengan pergerakan harga riil
                  </p>
                </div>
                <div className="flex gap-2 shrink-0">
                  {(["sep", "apr"] as const).map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`text-[11px] px-3 py-1.5 rounded-lg font-semibold transition-colors whitespace-nowrap ${
                        activeTab === tab ? "bg-blue-600 text-white shadow-sm" : "bg-slate-100 text-slate-500 hover:bg-slate-200"
                      }`}
                    >
                      {tab === "sep" ? "Apr → Sep 2025" : "Apr 2025 → Apr 2026"}
                    </button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent className="px-6 pb-6 space-y-6">

              {/* Scatter Plot */}
              <div className="bg-slate-50 rounded-xl p-4">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest mb-1">
                  Scatter Plot Distribusi Rank
                </p>
                <p className="text-[11px] text-slate-400 mb-4">
                  Sumbu X = Rank TOPSIS · Sumbu Y = Rank Return Aktual
                </p>
                <ResponsiveContainer width="100%" height={260}>
                  <ScatterChart margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis
                      type="number"
                      dataKey="x"
                      domain={[0.5, 7.5]}
                      ticks={[1, 2, 3, 4, 5, 6, 7]}
                      tick={{ fontSize: 11, fill: "#64748b" }}
                      axisLine={false}
                      tickLine={false}
                    >
                      <Label value="Rank TOPSIS" offset={-10} position="insideBottom" style={{ fontSize: 11, fill: "#94a3b8", fontWeight: 600 }} />
                    </XAxis>
                    <YAxis
                      type="number"
                      dataKey="y"
                      domain={[0.5, 7.5]}
                      ticks={[1, 2, 3, 4, 5, 6, 7]}
                      tick={{ fontSize: 11, fill: "#64748b" }}
                      axisLine={false}
                      tickLine={false}
                      width={28}
                    >
                      <Label value="Rank Return Aktual" angle={-90} position="insideLeft" style={{ fontSize: 11, fill: "#94a3b8", fontWeight: 600 }} />
                    </YAxis>
                    <ZAxis dataKey="z" range={[60, 60]} />
                    <Tooltip
                      cursor={{ strokeDasharray: "3 3" }}
                      content={({ payload }) => {
                        if (!payload?.length) return null;
                        const d = payload[0].payload;
                        return (
                          <div className="bg-white border border-slate-200 rounded-lg px-3 py-2 shadow-lg text-xs">
                            <p className="font-bold text-slate-800">{d.kode}</p>
                            <p className="text-slate-500">Rank TOPSIS: <span className="font-semibold text-blue-600">{d.x}</span></p>
                            <p className="text-slate-500">Rank Return: <span className="font-semibold text-emerald-600">{d.y}</span></p>
                          </div>
                        );
                      }}
                    />
                    <Scatter data={scatterData} shape={<CustomDot />} />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>

              {/* Comparison Table */}
              <div className="overflow-x-auto">
                <Table className="min-w-[480px]">
                  <TableHeader>
                    <TableRow className="bg-slate-50 hover:bg-slate-50 border-b border-slate-200">
                      {["Emiten", "Rank TOPSIS", "Rank Return Aktual", "Perubahan Posisi"].map((h, i) => (
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
                    {[...STOCKS]
                      .sort((a, b) => a.rankTopsis - b.rankTopsis)
                      .map((s) => {
                        const rankAktual = activeTab === "sep" ? s.rankApr2025vsSep2025 : s.rankApr2025vsApr2026;
                        return (
                          <TableRow key={s.kode} className="hover:bg-slate-50/80 border-b border-slate-100">
                            <TableCell className="pl-4 py-3">
                              <p className="font-bold text-slate-800 text-sm">{s.kode}</p>
                              <p className="text-[11px] text-slate-400">{s.nama}</p>
                            </TableCell>
                            <TableCell className="text-center py-3"><RankBadge rank={s.rankTopsis} /></TableCell>
                            <TableCell className="text-center py-3"><RankBadge rank={rankAktual} /></TableCell>
                            <TableCell className="text-center py-3">
                              <RankDelta rankA={s.rankTopsis} rankB={rankAktual} />
                            </TableCell>
                          </TableRow>
                        );
                      })}
                  </TableBody>
                </Table>
              </div>

              {/* H0 Note */}
              <div className="rounded-xl bg-amber-50 border border-amber-100 px-5 py-4">
                <p className="text-[11px] font-bold text-amber-700 uppercase tracking-widest mb-1">Interpretasi Hasil</p>
                <p className="text-[12px] text-amber-800 leading-relaxed">
                  Distribusi titik pada scatter plot tidak membentuk pola linear, mengindikasikan tidak terdapat korelasi antara peringkat fundamental TOPSIS dengan return harga saham aktual. Hasil ini konsisten dengan penerimaan <strong>H₀</strong> dan mencerminkan pengaruh faktor makroekonomi eksternal — fluktuasi harga komoditas global dan volatilitas sektor energi 2025–2026 — yang berada di luar cakupan model fundamental sistem ini.
                </p>
              </div>

            </CardContent>
          </Card>
        </section>

        {/* ── FOOTER ── */}
        <footer className="text-center py-8 border-t border-slate-200">
          <p className="text-[11px] text-slate-400 tracking-wide">
            Sistem Pendukung Keputusan Investasi Saham · Sektor Energi LQ45 · {META.periodeData} · Universitas Bina Nusantara 2026
          </p>
        </footer>
      </div>
    </main>
  );
}