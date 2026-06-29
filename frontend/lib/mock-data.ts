import { ENTROPY_WEIGHTS, META, STOCKS } from "@/lib/data";
import type { DashboardData } from "@/lib/types";

export function getMockDashboardData(): DashboardData {
  const undervaluedCount = STOCKS.filter(
    (stock) => stock.klasifikasi === "Undervalued",
  ).length;

  return {
    stocks: STOCKS,
    entropyWeights: ENTROPY_WEIGHTS,
    meta: META,
    summary: {
      totalEmiten: STOCKS.length,
      lolosGraham: undervaluedCount,
      dominanBobot: "EPS",
    },
  };
}
