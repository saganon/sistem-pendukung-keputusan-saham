import math

class GrahamFormula:
    @staticmethod
    def calculate(eps: float, bvps: float):
        graham_number = math.sqrt(22.5 * eps * bvps)

        return round(graham_number, 2)
