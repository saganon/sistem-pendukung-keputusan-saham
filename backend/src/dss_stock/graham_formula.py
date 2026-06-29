import math


class GrahamFormula:
    """Benjamin Graham Number: GN = sqrt(22.5 x EPS x BVPS)."""

    GRAHAM_CONSTANT = 22.5

    @staticmethod
    def calculate(eps: float, bvps: float) -> float:
        return math.sqrt(GrahamFormula.GRAHAM_CONSTANT * eps * bvps)

    @staticmethod
    def is_applicable(eps: float | None, bvps: float | None) -> bool:
        return eps is not None and bvps is not None and eps > 0 and bvps > 0

    @staticmethod
    def classify(
        current_price: float | None,
        graham_number: float,
    ) -> str:
        if graham_number <= 0 or current_price is None:
            return "tidak_valid"
        if current_price < graham_number:
            return "undervalued"
        return "overvalued"
