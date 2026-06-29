import { API_BASE_URL } from "@/lib/config";
import type { DashboardData, Klasifikasi, Stock } from "@/lib/types";

type ApiAnalysisResponse = {
  meta: DashboardData["meta"];
  entropyWeights: DashboardData["entropyWeights"];
  summary: DashboardData["summary"];
  stocks: Array<Partial<Stock> & Pick<Stock, "kode" | "nama">>;
};

function toNumber(value: unknown, fallback = 0): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function normalizeStock(raw: ApiAnalysisResponse["stocks"][number]): Stock {
  return {
    kode: raw.kode,
    nama: raw.nama,
    eps: toNumber(raw.eps),
    bvps: toNumber(raw.bvps),
    roa: toNumber(raw.roa),
    der: toNumber(raw.der),
    pbv: toNumber(raw.pbv),
    hargaPasar: toNumber(raw.hargaPasar),
    grahamNumber: toNumber(raw.grahamNumber),
    klasifikasi: (raw.klasifikasi as Klasifikasi) ?? "Undervalued",
    jarakPositif: toNumber(raw.jarakPositif),
    jarakNegatif: toNumber(raw.jarakNegatif),
    skorTopsis: toNumber(raw.skorTopsis),
    rankTopsis: toNumber(raw.rankTopsis, 999),
    rankApr2025vsSep2025: toNumber(raw.rankApr2025vsSep2025, 999),
    rankApr2025vsApr2026: toNumber(raw.rankApr2025vsApr2026, 999),
  };
}

export async function fetchDashboardDataFromApi(): Promise<DashboardData> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analysis`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(
      `Gagal mengambil data analisis (${response.status} ${response.statusText})`,
    );
  }

  const data = (await response.json()) as ApiAnalysisResponse;

  return {
    meta: data.meta,
    entropyWeights: data.entropyWeights,
    summary: data.summary,
    stocks: data.stocks.map(normalizeStock),
  };
}
