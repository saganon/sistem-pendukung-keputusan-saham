"""Konstanta domain yang dipakai lintas modul backend."""

STOCK_NAMES: dict[str, str] = {
    "ADMR": "Alamtri Minerals Indonesia Tbk.",
    "ADRO": "Alamtri Resources Indonesia Tbk.",
    "AKRA": "AKR Corporindo Tbk.",
    "ITMG": "Indo Tambangraya Megah Tbk.",
    "MEDC": "Medco Energi Internasional Tbk.",
    "PGAS": "Perusahaan Gas Negara (Persero) Tbk.",
    "PTBA": "Bukit Asam (Persero) Tbk.",
}

CRITERIA_LABELS: dict[str, str] = {
    "ROA": "Return on Assets (ROA)",
    "DER": "Debt to Equity Ratio (DER)",
    "PBV": "Price to Book Value (PBV)",
    "EPS": "Earnings Per Share (EPS)",
}

CRITERIA_TYPES: dict[str, str] = {
    "ROA": "benefit",
    "DER": "cost",
    "PBV": "cost",
    "EPS": "benefit",
}

BACKTESTING_PERIODS = (
    {
        "label": "Apr 2025 → Sep 2025",
        "key": "rankApr2025vsSep2025",
        "startDate": "2025-04-08",
        "endDate": "2025-09-01",
    },
    {
        "label": "Apr 2025 → Apr 2026",
        "key": "rankApr2025vsApr2026",
        "startDate": "2025-04-08",
        "endDate": "2026-04-01",
    },
)
