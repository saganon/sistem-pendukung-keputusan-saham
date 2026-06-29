"""Aplikasi FastAPI backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dss_stock.api.router import router

app = FastAPI(
    title="Sistem Pendukung Keputusan Saham API",
    description=(
        "API backend untuk dashboard analisis saham sektor energi "
        "(Graham Number, Entropy, TOPSIS, Backtesting)."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "message": "Sistem Pendukung Keputusan Saham API",
        "docs": "/docs",
        "health": "/api/v1/health",
        "analysis": "/api/v1/analysis",
    }
