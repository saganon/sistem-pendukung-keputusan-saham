"""Orkestrasi pipeline analisis untuk kebutuhan API."""

from datetime import datetime

from dss_stock.audit_input import FISCAL_YEAR, PUBLICATION_YEAR, STOCK_VALUATION_DATE
from dss_stock.calculate_entropy_weight import build_decision_matrix, calculate_entropy_steps
from dss_stock.calculate_topsis import CRITERIA_TYPES, calculate_topsis_steps
from dss_stock.constants import BACKTESTING_PERIODS, STOCK_NAMES
from dss_stock.entity.stock_info import StockInfo
from dss_stock.services.backtesting_service import calculate_backtesting_ranks
from dss_stock.under_value_stock import screen_graham_undervalued

_last_all_results: list[StockInfo] = []
_last_undervalued: list[StockInfo] = []
_last_entropy_steps = None
_last_topsis_steps = None


def _format_klasifikasi(status: str) -> str:
    mapping = {
        "undervalued": "Undervalued",
        "overvalued": "Overvalued",
        "tidak_valid": "Tidak Valid",
    }
    return mapping.get(status, status)


def _dataframe_to_nested_dict(df) -> dict[str, dict[str, float]]:
    return {
        str(index): {str(column): float(value) for column, value in row.items()}
        for index, row in df.iterrows()
    }


def _series_to_dict(series) -> dict[str, float]:
    return {str(key): float(value) for key, value in series.items()}


def _format_tanggal_harga() -> str:
    date = datetime.strptime(STOCK_VALUATION_DATE, "%Y-%m-%d")
    months = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember",
    }
    return f"{date.day} {months[date.month]} {date.year}"


def _stock_to_graham_payload(stock: StockInfo) -> dict:
    return {
        "kode": stock.stock_code,
        "nama": STOCK_NAMES.get(stock.stock_code, stock.stock_code),
        "eps": round(stock.eps or 0, 2),
        "bvps": round(stock.bvps or 0, 2),
        "roa": round((stock.return_on_assets or 0) * 100, 2),
        "der": round(stock.debt_to_equity or 0, 2),
        "pbv": round(stock.price_to_book or 0, 2),
        "hargaPasar": round(stock.stock_price or 0, 2),
        "grahamNumber": round(stock.graham_number, 2),
        "klasifikasi": _format_klasifikasi(stock.valuation_status),
    }


def run_analysis_pipeline() -> None:
    """Jalankan pipeline lengkap dan simpan hasil di memori modul."""
    global _last_all_results, _last_undervalued, _last_entropy_steps, _last_topsis_steps

    undervalued, all_results = screen_graham_undervalued(sleep_seconds=0)
    _last_all_results = all_results
    _last_undervalued = undervalued
    _last_entropy_steps = None
    _last_topsis_steps = None

    if len(undervalued) >= 2:
        decision_matrix = build_decision_matrix(undervalued)
        _last_entropy_steps = calculate_entropy_steps(decision_matrix)
        _last_topsis_steps = calculate_topsis_steps(
            decision_matrix,
            _last_entropy_steps.weights,
            CRITERIA_TYPES,
        )


def get_graham_screening() -> list[dict]:
    if not _last_all_results:
        run_analysis_pipeline()
    return [_stock_to_graham_payload(stock) for stock in _last_all_results]


def get_entropy_result() -> dict:
    if not _last_entropy_steps:
        run_analysis_pipeline()
    if _last_entropy_steps is None:
        raise ValueError("Entropy membutuhkan minimal 2 saham undervalued.")

    steps = _last_entropy_steps
    return {
        "decisionMatrix": _dataframe_to_nested_dict(steps.decision_matrix),
        "columnTotals": _series_to_dict(steps.column_totals),
        "proportionMatrix": _dataframe_to_nested_dict(steps.proportion_matrix),
        "entropy": _series_to_dict(steps.entropy),
        "diversification": _series_to_dict(steps.diversification),
        "weights": {
            "roa": float(steps.weights["ROA"]),
            "der": float(steps.weights["DER"]),
            "pbv": float(steps.weights["PBV"]),
            "eps": float(steps.weights["EPS"]),
        },
        "kConstant": float(steps.k_constant),
        "nAlternatives": int(steps.n_alternatives),
    }


def get_entropy_weights() -> dict[str, float]:
    return get_entropy_result()["weights"]


def get_dashboard_stocks() -> list[dict]:
    if not _last_undervalued:
        run_analysis_pipeline()
    if not _last_undervalued:
        return []

    topsis_by_code = {}
    if _last_topsis_steps is not None:
        for stock_code in _last_topsis_steps.closeness_score.index:
            topsis_by_code[stock_code] = {
                "jarakPositif": float(
                    _last_topsis_steps.distance_positive.loc[stock_code]
                ),
                "jarakNegatif": float(
                    _last_topsis_steps.distance_negative.loc[stock_code]
                ),
                "skorTopsis": float(_last_topsis_steps.closeness_score.loc[stock_code]),
                "rankTopsis": int(_last_topsis_steps.ranking.loc[stock_code]),
            }

    backtesting = calculate_backtesting_ranks(
        [stock.stock_code for stock in _last_undervalued]
    )

    stocks: list[dict] = []
    for stock in _last_undervalued:
        payload = _stock_to_graham_payload(stock)
        payload.update(topsis_by_code.get(stock.stock_code, {}))
        backtest = backtesting.get(stock.stock_code, {})
        payload.update(
            {
                "returnApr2025vsSep2025": backtest.get("returnApr2025vsSep2025"),
                "returnApr2025vsApr2026": backtest.get("returnApr2025vsApr2026"),
                "rankApr2025vsSep2025": backtest.get("rankApr2025vsSep2025"),
                "rankApr2025vsApr2026": backtest.get("rankApr2025vsApr2026"),
            }
        )
        stocks.append(payload)

    stocks.sort(key=lambda item: item.get("rankTopsis", 999))
    return stocks


def get_topsis_result() -> dict:
    if not _last_topsis_steps:
        run_analysis_pipeline()
    if _last_topsis_steps is None:
        raise ValueError("TOPSIS membutuhkan minimal 2 saham undervalued.")

    steps = _last_topsis_steps
    return {
        "decisionMatrix": _dataframe_to_nested_dict(steps.decision_matrix),
        "entropyWeights": get_entropy_weights(),
        "normFactor": _series_to_dict(steps.norm_factor),
        "normalizedMatrix": _dataframe_to_nested_dict(steps.normalized_matrix),
        "weightedMatrix": _dataframe_to_nested_dict(steps.weighted_matrix),
        "idealPositive": _series_to_dict(steps.ideal_positive),
        "idealNegative": _series_to_dict(steps.ideal_negative),
        "ranking": get_dashboard_stocks(),
    }


def get_analysis_response() -> dict:
    if not _last_all_results:
        run_analysis_pipeline()

    weights = (
        get_entropy_weights()
        if _last_entropy_steps
        else {"roa": 0.0, "der": 0.0, "pbv": 0.0, "eps": 0.0}
    )
    dominan = max(weights, key=weights.get)

    return {
        "meta": {
            "periodeData": f"Februari – April {PUBLICATION_YEAR}",
            "tanggalHarga": _format_tanggal_harga(),
            "sumberData": "Yahoo Finance & IDX",
            "tahunLaporan": str(FISCAL_YEAR),
            "backtesting": [
                {"label": period["label"], "key": period["key"]}
                for period in BACKTESTING_PERIODS
            ],
        },
        "entropyWeights": weights,
        "summary": {
            "totalEmiten": len(_last_all_results),
            "lolosGraham": sum(
                1
                for stock in _last_all_results
                if stock.valuation_status == "undervalued"
            ),
            "dominanBobot": dominan.upper(),
        },
        "stocks": get_dashboard_stocks(),
        "grahamScreening": get_graham_screening(),
    }


def get_backtesting_response() -> dict:
    stocks = get_dashboard_stocks()
    return {
        "meta": get_analysis_response()["meta"],
        "stocks": [
            {
                "kode": stock["kode"],
                "nama": stock["nama"],
                "rankTopsis": stock.get("rankTopsis"),
                "returnApr2025vsSep2025": stock.get("returnApr2025vsSep2025"),
                "returnApr2025vsApr2026": stock.get("returnApr2025vsApr2026"),
                "rankApr2025vsSep2025": stock.get("rankApr2025vsSep2025"),
                "rankApr2025vsApr2026": stock.get("rankApr2025vsApr2026"),
            }
            for stock in stocks
        ],
    }
