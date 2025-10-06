# reports/utils/calculations.py

from typing import Iterable

def average(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0

def percentage(score: float, total: float = 100.0) -> float:
    return round((score / total) * 100, 2) if total else 0.0
