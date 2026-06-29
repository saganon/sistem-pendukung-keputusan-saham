export type DataSource = "api" | "mock";

/** Ubah ke `"mock"` untuk pakai `lib/data.ts` tanpa backend. */
export const DATA_SOURCE = (process.env.NEXT_PUBLIC_DATA_SOURCE ?? "api") as DataSource;

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
