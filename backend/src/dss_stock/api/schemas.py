"""Skema response API — diselaraskan dengan `frontend/lib/data.ts`."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CamelModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, ser_json_by_alias=True)


class BacktestingPeriodSchema(CamelModel):
    label: str
    key: str


class MetaSchema(CamelModel):
    periode_data: str = Field(alias="periodeData")
    tanggal_harga: str = Field(alias="tanggalHarga")
    sumber_data: str = Field(alias="sumberData")
    tahun_laporan: str = Field(alias="tahunLaporan")
    backtesting: list[BacktestingPeriodSchema]


class EntropyWeightsSchema(CamelModel):
    roa: float
    der: float
    pbv: float
    eps: float


class StockDashboardSchema(CamelModel):
    """Bentuk data per saham yang dikonsumsi dashboard frontend."""

    kode: str
    nama: str
    eps: float
    bvps: float
    roa: float
    der: float
    pbv: float
    harga_pasar: float = Field(alias="hargaPasar")
    graham_number: float = Field(alias="grahamNumber")
    klasifikasi: str
    jarak_positif: float | None = Field(default=None, alias="jarakPositif")
    jarak_negatif: float | None = Field(default=None, alias="jarakNegatif")
    skor_topsis: float | None = Field(default=None, alias="skorTopsis")
    rank_topsis: int | None = Field(default=None, alias="rankTopsis")
    rank_apr_2025_vs_sep_2025: int | None = Field(
        default=None, alias="rankApr2025vsSep2025"
    )
    rank_apr_2025_vs_apr_2026: int | None = Field(
        default=None, alias="rankApr2025vsApr2026"
    )


class GrahamStockSchema(CamelModel):
    kode: str
    nama: str
    eps: float
    bvps: float
    roa: float
    der: float
    pbv: float
    harga_pasar: float = Field(alias="hargaPasar")
    graham_number: float = Field(alias="grahamNumber")
    klasifikasi: str


class AnalysisSummarySchema(CamelModel):
    total_emiten: int = Field(alias="totalEmiten")
    lolos_graham: int = Field(alias="lolosGraham")
    dominan_bobot: str = Field(alias="dominanBobot")


class AnalysisResponseSchema(CamelModel):
    """Payload utama — mirror `STOCKS`, `ENTROPY_WEIGHTS`, `META` di frontend."""

    meta: MetaSchema
    entropy_weights: EntropyWeightsSchema = Field(alias="entropyWeights")
    summary: AnalysisSummarySchema
    stocks: list[StockDashboardSchema]
    graham_screening: list[GrahamStockSchema] = Field(alias="grahamScreening")


class HealthResponseSchema(CamelModel):
    status: str
    timestamp: datetime


class EntropyStepTablesSchema(CamelModel):
    decision_matrix: dict[str, dict[str, float]] = Field(alias="decisionMatrix")
    column_totals: dict[str, float] = Field(alias="columnTotals")
    proportion_matrix: dict[str, dict[str, float]] = Field(alias="proportionMatrix")
    entropy: dict[str, float]
    diversification: dict[str, float]
    weights: EntropyWeightsSchema
    k_constant: float = Field(alias="kConstant")
    n_alternatives: int = Field(alias="nAlternatives")


class TopsisStepTablesSchema(CamelModel):
    decision_matrix: dict[str, dict[str, float]] = Field(alias="decisionMatrix")
    entropy_weights: EntropyWeightsSchema = Field(alias="entropyWeights")
    norm_factor: dict[str, float] = Field(alias="normFactor")
    normalized_matrix: dict[str, dict[str, float]] = Field(alias="normalizedMatrix")
    weighted_matrix: dict[str, dict[str, float]] = Field(alias="weightedMatrix")
    ideal_positive: dict[str, float] = Field(alias="idealPositive")
    ideal_negative: dict[str, float] = Field(alias="idealNegative")
    ranking: list[StockDashboardSchema]


class BacktestingStockSchema(CamelModel):
    kode: str
    nama: str
    rank_topsis: int = Field(alias="rankTopsis")
    return_apr_2025_vs_sep_2025: float = Field(alias="returnApr2025vsSep2025")
    return_apr_2025_vs_apr_2026: float = Field(alias="returnApr2025vsApr2026")
    rank_apr_2025_vs_sep_2025: int = Field(alias="rankApr2025vsSep2025")
    rank_apr_2025_vs_apr_2026: int = Field(alias="rankApr2025vsApr2026")


class BacktestingResponseSchema(CamelModel):
    meta: MetaSchema
    stocks: list[BacktestingStockSchema]
