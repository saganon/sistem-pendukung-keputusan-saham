import { fetchDashboardDataFromApi } from "@/lib/api-client";
import { DATA_SOURCE } from "@/lib/config";
import { getMockDashboardData } from "@/lib/mock-data";
import type { DashboardData } from "@/lib/types";

export async function getDashboardData(): Promise<DashboardData> {
  if (DATA_SOURCE === "mock") {
    return getMockDashboardData();
  }

  return fetchDashboardDataFromApi();
}
