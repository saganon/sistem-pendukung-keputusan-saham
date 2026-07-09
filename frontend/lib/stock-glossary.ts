export type StockInfo = {
  kode: string;
  nama: string;
  /** Penjelasan huruf-huruf dalam kode saham */
  artiSingkatan: string;
  bidangUsaha: string;
  deskripsi: string;
};

export const STOCK_GLOSSARY: Record<string, StockInfo> = {
  ADMR: {
    kode: "ADMR",
    nama: "Alamtri Minerals Indonesia Tbk.",
    artiSingkatan:
      "Alamtri Minerals — kode resmi emiten grup pertambangan mineral Alamtri di Bursa Efek Indonesia (dulu dikenal sebagai Adaro Minerals)",
    bidangUsaha: "Pertambangan batubara & mineral",
    deskripsi:
      "Perusahaan tambang batubara dan mineral yang merupakan bagian dari grup Alamtri. Saham ini mencatatkan diri di BEI dengan kode ADMR.",
  },
  ADRO: {
    kode: "ADRO",
    nama: "Alamtri Resources Indonesia Tbk.",
    artiSingkatan:
      "Alamtri Resources — berasal dari nama lama Adaro Energy, kini berganti nama menjadi Alamtri Resources Indonesia",
    bidangUsaha: "Pertambangan batubara",
    deskripsi:
      "Salah satu produsen batubara terbesar di Indonesia. Kode ADRO adalah singkatan resmi perusahaan ini di bursa saham.",
  },
  AKRA: {
    kode: "AKRA",
    nama: "AKR Corporindo Tbk.",
    artiSingkatan:
      "AKR — diambil langsung dari nama perusahaan AKR Corporindo",
    bidangUsaha: "Distribusi BBM & infrastruktur energi",
    deskripsi:
      "Perusahaan yang bergerak di bidang distribusi bahan bakar minyak (BBM), logistik, dan infrastruktur pelabuhan. Kode AKRA sama dengan nama brand perusahaan.",
  },
  ITMG: {
    kode: "ITMG",
    nama: "Indo Tambangraya Megah Tbk.",
    artiSingkatan:
      "Indo Tambangraya Megah — singkatan dari nama lengkap perusahaan: I-T-M-G",
    bidangUsaha: "Pertambangan batubara",
    deskripsi:
      "Perusahaan tambang batubara yang merupakan anak perusahaan grup Banpu Thailand. Kode ITMG merepresentasikan inisial nama perusahaan.",
  },
  MEDC: {
    kode: "MEDC",
    nama: "Medco Energi Internasional Tbk.",
    artiSingkatan:
      "Medco Energi — singkatan dari nama perusahaan Medco Energi",
    bidangUsaha: "Eksplorasi & produksi minyak dan gas bumi",
    deskripsi:
      "Perusahaan energi yang berfokus pada eksplorasi dan produksi migas (oil & gas). Kode MEDC adalah singkatan resmi Medco Energi di BEI.",
  },
  PGAS: {
    kode: "PGAS",
    nama: "Perusahaan Gas Negara (Persero) Tbk.",
    artiSingkatan:
      "Perusahaan Gas — P-GAS, singkatan dari Perusahaan Gas Negara",
    bidangUsaha: "Distribusi & transmisi gas bumi",
    deskripsi:
      "Badan usaha milik negara (BUMN) yang mengelola pipa gas bumi di Indonesia. Kode PGAS berarti Perusahaan GAS Negara.",
  },
  PTBA: {
    kode: "PTBA",
    nama: "Bukit Asam (Persero) Tbk.",
    artiSingkatan:
      "PT Bukit Asam — P-T-B-A, singkatan dari PT Bukit Asam Tbk.",
    bidangUsaha: "Pertambangan batubara",
    deskripsi:
      "BUMN pertambangan batubara tertua di Indonesia, berlokasi di Tanjung Enim, Sumatera Selatan. Kode PTBA adalah inisial PT Bukit Asam.",
  },
};

export function getStockInfo(kode: string): StockInfo | undefined {
  return STOCK_GLOSSARY[kode.toUpperCase()];
}
