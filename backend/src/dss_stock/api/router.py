"""Router HTTP API backend."""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from dss_stock.api.schemas import (
    AnalysisResponseSchema,
    BacktestingResponseSchema,
    EntropyStepTablesSchema,
    EntropyWeightsSchema,
    GrahamStockSchema,
    HealthResponseSchema,
    MetaSchema,
    TopsisStepTablesSchema,
)
from dss_stock.services import analysis_service

router = APIRouter(prefix="/api/v1")


@router.get("/health", response_model=HealthResponseSchema, tags=["system"])
def health_check() -> HealthResponseSchema:
    return HealthResponseSchema(
        status="ok",
        timestamp=datetime.now(timezone.utc),
    )


@router.get(
    "/analysis",
    response_model=AnalysisResponseSchema,
    tags=["analysis"],
    summary="Payload lengkap dashboard frontend",
)
def get_analysis() -> AnalysisResponseSchema:
    """Mengembalikan struktur yang setara dengan `frontend/lib/data.ts`."""
    return AnalysisResponseSchema.model_validate(analysis_service.get_analysis_response())


@router.get(
    "/graham",
    response_model=list[GrahamStockSchema],
    tags=["graham"],
    summary="Hasil screening Benjamin Graham semua emiten",
)
def get_graham_screening() -> list[GrahamStockSchema]:
    return [
        GrahamStockSchema.model_validate(item)
        for item in analysis_service.get_graham_screening()
    ]


@router.get(
    "/entropy",
    response_model=EntropyStepTablesSchema,
    tags=["entropy"],
    summary="Bobot Entropy dan tabel per langkah",
)
def get_entropy() -> EntropyStepTablesSchema:
    try:
        return EntropyStepTablesSchema.model_validate(analysis_service.get_entropy_result())
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get(
    "/entropy/weights",
    response_model=EntropyWeightsSchema,
    tags=["entropy"],
    summary="Bobot Entropy final saja",
)
def get_entropy_weights() -> EntropyWeightsSchema:
    try:
        return EntropyWeightsSchema.model_validate(analysis_service.get_entropy_weights())
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get(
    "/topsis",
    response_model=TopsisStepTablesSchema,
    tags=["topsis"],
    summary="Peringkat TOPSIS dan tabel per langkah",
)
def get_topsis() -> TopsisStepTablesSchema:
    try:
        return TopsisStepTablesSchema.model_validate(analysis_service.get_topsis_result())
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get(
    "/backtesting",
    response_model=BacktestingResponseSchema,
    tags=["backtesting"],
    summary="Ranking backtesting return harga historis",
)
def get_backtesting() -> BacktestingResponseSchema:
    return BacktestingResponseSchema.model_validate(
        analysis_service.get_backtesting_response()
    )
