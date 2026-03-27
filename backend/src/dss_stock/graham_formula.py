import math

class GrahamFormula:
    @staticmethod
    def calculate(eps: float, bvps: float):
        v = math.sqrt(22.5 * eps * bvps)
        return v
