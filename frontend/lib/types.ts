export type Klasifikasi = "Undervalued" | "Overvalued" | "Tidak Valid";

export type Stock = {
  kode: string;
  nama: string;
  eps: number;
  bvps: number;
  roa: number;
  der: number;
  pbv: number;
  hargaPasar: number;
  grahamNumber: number;
  klasifikasi: Klasifikasi;
  jarakPositif: number;
  jarakNegatif: number;
  skorTopsis: number;
  rankTopsis: number;
  rankApr2025vsSep2025: number;
  rankApr2025vsApr2026: number;
};

export type EntropyWeights = {
  roa: number;
  der: number;
  pbv: number;
  eps: number;
};

export type BacktestingPeriod = {
  label: string;
  key: string;
};

export type Meta = {
  periodeData: string;
  tanggalHarga: string;
  sumberData: string;
  tahunLaporan: string;
  backtesting: BacktestingPeriod[];
};

export type AnalysisSummary = {
  totalEmiten: number;
  lolosGraham: number;
  dominanBobot: string;
};

export type DashboardData = {
  stocks: Stock[];
  entropyWeights: EntropyWeights;
  meta: Meta;
  summary: AnalysisSummary;
};
