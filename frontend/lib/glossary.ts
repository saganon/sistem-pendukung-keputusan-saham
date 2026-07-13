export type InfoSection = {
  heading: string;
  body?: string;
  items?: string[];
  technical?: string;
};

export type InfoContent = {
  title: string;
  sections: InfoSection[];
};

export const CRITERIA_FRIENDLY: Record<string, string> = {
  EPS: "Keuntungan per Saham",
  DER: "Tingkat Utang",
  ROA: "Efisiensi Aset",
  PBV: "Harga vs Nilai Buku",
};

export const INFO_CONTENT: Record<string, InfoContent> = {
  "kode-saham": {
    title: "Apa itu kode saham?",
    sections: [
      {
        heading: "Kode saham itu apa?",
        body: "Kode saham adalah singkatan 4 huruf yang mewakili nama perusahaan di Bursa Efek Indonesia (BEI). Contoh: ADRO untuk Alamtri Resources, PGAS untuk Perusahaan Gas Negara. Kode ini digunakan saat membeli atau menjual saham melalui aplikasi sekuritas.",
      },
      {
        heading: "Mengapa penting dipahami?",
        items: [
          "Kode memudahkan identifikasi perusahaan di aplikasi sekuritas",
          "Satu kode = satu emiten (perusahaan terbuka) di bursa",
          "Kode tidak selalu sama persis dengan nama perusahaan — ada yang disingkat",
        ],
      },
      {
        heading: "Contoh dalam analisis ini",
        body: "Sistem menganalisis 7 saham sektor energi dari indeks LQ45. Setiap kode di bawah ini mewakili satu perusahaan energi yang diperdagangkan di BEI.",
      },
    ],
  },
  overview: {
    title: "Bagaimana analisis ini bekerja?",
    sections: [
      {
        heading: "Apa yang dilakukan sistem?",
        body: "Sistem ini membantu membandingkan beberapa saham energi terpilih dengan empat langkah: menilai apakah harganya masih murah, menentukan faktor keuangan mana yang paling berpengaruh, memberikan peringkat objektif, lalu menguji apakah peringkat tersebut sesuai dengan kenaikan harga nyata.",
      },
      {
        heading: "Langkah analisis",
        items: [
          "Filter harga wajar — hanya saham yang dinilai masih murah",
          "Penentuan bobot faktor — faktor dengan variasi terbesar mendapat bobot tertinggi",
          "Peringkat objektif — saham dinilai secara menyeluruh dan diurutkan",
          "Pengujian hasil — peringkat dibandingkan dengan kenaikan harga aktual",
        ],
        body: "",
      },
      {
        heading: "Penting untuk diketahui",
        body: "Hasil ini adalah alat bantu analisis, bukan saran untuk membeli atau menjual saham. Selalu lakukan riset sendiri sebelum berinvestasi.",
      },
    ],
  },
  graham: {
    title: "Bagaimana harga wajar dihitung?",
    sections: [
      {
        heading: "Apa yang dibandingkan?",
        body: "Sistem membandingkan harga saham di pasar saat ini dengan perkiraan harga wajar berdasarkan rumus Benjamin Graham, seorang investor terkenal yang dikenal dengan pendekatan valuasi fundamental.",
      },
      {
        heading: "Cara membaca grafik",
        items: [
          "Batang hijau = harga saham saat ini di pasar",
          "Batang biru = perkiraan harga wajar",
          "Jika hijau lebih pendek dari biru → saham dinilai masih murah",
        ],
        body: "",
      },
      {
        heading: "Rumus (detail teknis)",
        technical:
          "Graham Number = √(22,5 × Laba per Saham × Nilai Buku per Saham)\n\nJika Harga Pasar < Graham Number → saham diklasifikasi sebagai undervalued (masih murah).",
      },
    ],
  },
  entropy: {
    title: "Bagaimana bobot faktor ditentukan?",
    sections: [
      {
        heading: "Apa yang dilakukan?",
        body: "Sistem menganalisis variasi data keuangan dari semua saham yang dibandingkan. Faktor yang paling bervariasi antar saham mendapat bobot tertinggi, karena lebih mampu membedakan saham yang baik dan kurang baik.",
      },
      {
        heading: "Mengapa tanpa preferensi subjektif?",
        body: "Bobot tidak ditentukan secara manual oleh analis. Semua faktor dievaluasi secara objektif dari data yang tersedia, sehingga hasilnya konsisten dan dapat diulang.",
      },
      {
        heading: "Rumus (detail teknis)",
        technical:
          "Metode Entropy Weight:\n1. Normalisasi matriks keputusan\n2. Hitung proporsi dan entropi setiap kriteria\n3. Hitung degree of diversification (d)\n4. Bobot wⱼ = dⱼ / Σdⱼ",
      },
    ],
  },
  eps: {
    title: "Keuntungan per Saham (EPS)",
    sections: [
      {
        heading: "Apa itu?",
        body: "EPS (Earnings Per Share) menunjukkan berapa banyak laba bersih yang dihasilkan per lembar saham. Semakin tinggi EPS, semakin besar keuntungan yang dihasilkan per saham.",
      },
      {
        heading: "Cara membaca",
        body: "Nilai ditampilkan dalam Rupiah. Semakin tinggi semakin baik — saham dengan EPS tinggi cenderung lebih menguntungkan bagi pemegang saham.",
      },
    ],
  },
  der: {
    title: "Tingkat Utang (DER)",
    sections: [
      {
        heading: "Apa itu?",
        body: "DER (Debt to Equity Ratio) mengukur seberapa besar utang perusahaan dibandingkan dengan modal sendiri. Rasio ini menunjukkan tingkat ketergantungan perusahaan pada pinjaman.",
      },
      {
        heading: "Cara membaca",
        body: "Semakin rendah semakin baik. DER tinggi berarti perusahaan banyak berutang, yang bisa meningkatkan risiko jika kondisi bisnis memburuk.",
      },
    ],
  },
  roa: {
    title: "Efisiensi Aset (ROA)",
    sections: [
      {
        heading: "Apa itu?",
        body: "ROA (Return on Assets) mengukur seberapa efisien perusahaan menggunakan asetnya untuk menghasilkan laba. Persentase yang lebih tinggi menunjukkan penggunaan aset yang lebih produktif.",
      },
      {
        heading: "Cara membaca",
        body: "Ditampilkan dalam persen (%). Semakin tinggi semakin baik — perusahaan mampu menghasilkan lebih banyak laba dari aset yang dimilikinya.",
      },
    ],
  },
  pbv: {
    title: "Harga vs Nilai Buku (PBV)",
    sections: [
      {
        heading: "Apa itu?",
        body: "PBV (Price to Book Value) membandingkan harga saham di pasar dengan nilai buku per saham. Nilai buku mencerminkan aset bersih perusahaan per lembar saham.",
      },
      {
        heading: "Cara membaca",
        body: "Semakin rendah semakin baik. PBV rendah bisa mengindikasikan saham diperdagangkan di bawah nilai asetnya.",
      },
    ],
  },
  topsis: {
    title: "Bagaimana peringkat objektif dibuat?",
    sections: [
      {
        heading: "Apa yang dilakukan?",
        body: "Setiap saham yang lolos filter harga wajar dinilai berdasarkan empat faktor keuangan (keuntungan, utang, efisiensi aset, harga vs nilai buku) dengan bobot yang sudah ditentukan. Hasilnya adalah peringkat dari yang paling baik secara fundamental hingga yang paling rendah.",
      },
      {
        heading: "Cara membaca peringkat",
        items: [
          "Peringkat 1 = saham dengan penilaian keseluruhan terbaik",
          "Semakin tinggi skor → semakin dekat ke kondisi ideal",
          "Peringkat terakhir = penilaian keseluruhan paling rendah",
        ],
        body: "",
      },
      {
        heading: "Rumus (detail teknis)",
        technical:
          "Metode TOPSIS (Technique for Order Preference by Similarity to Ideal Solution):\n1. Normalisasi matriks keputusan\n2. Pembobotan dengan bobot entropy\n3. Hitung jarak ke solusi ideal positif (D⁺) dan negatif (D⁻)\n4. Skor Ci = D⁻ / (D⁺ + D⁻)",
      },
    ],
  },
  backtesting: {
    title: "Apa itu pengujian objektif?",
    sections: [
      {
        heading: "Apa yang diuji?",
        body: "Sistem membandingkan peringkat analisis (per April 2025) dengan peringkat kenaikan harga saham yang benar-benar terjadi setelahnya. Tujuannya: melihat apakah data fundamental sesuai dengan pergerakan harga nyata.",
      },
      {
        heading: "Cara membaca grafik",
        items: [
          "Sumbu horizontal = peringkat dari analisis sistem",
          "Sumbu vertikal = peringkat kenaikan harga nyata",
          "Jika titik membentuk garis naik → analisis cenderung akurat",
          "Jika titik tersebar acak → ada faktor lain di luar analisis fundamental",
        ],
        body: "",
      },
      {
        heading: "Kesimpulan praktis",
        body: "Gunakan hasil analisis sebagai salah satu referensi, bukan satu-satunya alasan untuk membeli saham. Harga saham juga dipengaruhi kondisi ekonomi, harga komoditas, dan berita pasar.",
      },
    ],
  },
};
