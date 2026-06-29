import { Dashboard } from "@/components/dashboard";
import { getDashboardData } from "@/lib/data-source";

export default async function Home() {
  const data = await getDashboardData();
  return <Dashboard data={data} />;
}
