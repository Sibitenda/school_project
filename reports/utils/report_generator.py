# reports/utils/report_generator.py

from typing import Dict
from .calculations import average

def compute_student_summary(marks_queryset) -> Dict[str, float]:
    """
    Accepts a Django queryset (StudentMark objects) and returns:
     - total_courses: int
     - average_gpa: float (rounded to 2 decimals)
    Pure function style: does computation, returns dict.
    """
    marks = list(marks_queryset)
    total = len(marks)
    if total == 0:
        return {"total_courses": 0, "average_gpa": 0.0}

    gpas = [m.gpa for m in marks if getattr(m, "gpa", None) is not None]
    avg_gpa = round(average(gpas), 2) if gpas else 0.0
    return {"total_courses": total, "average_gpa": avg_gpa}
