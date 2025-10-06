from typing import Tuple, List
from reports.utils.calculations import average


# -------------------------------
# Convert numeric score to letter + grade point
# -------------------------------
def get_letter_grade(score: float) -> str:
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B+"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    return "F"


def get_grade_point(score: float) -> float:
    if score >= 80:
        return 5.0
    elif score >= 70:
        return 4.5
    elif score >= 60:
        return 4.0
    elif score >= 50:
        return 3.0
    elif score >= 45:
        return 2.0
    return 0.0


# -------------------------------
# GPA / CPA calculations
# -------------------------------
def calculate_gpa(marks) -> float:
    """
    Compute GPA from StudentMark queryset or list of mark objects.
    """
    if not marks:
        return 0.0

    points = [get_grade_point(m.score) for m in marks]
    return round(average(points), 2)


def calculate_cpa(profile) -> float:
    """
    Compute cumulative performance average (same as CGPA).
    """
    from reports.models import StudentMark  # avoid circular import
    marks = StudentMark.objects.filter(student=profile)
    return calculate_gpa(marks)


# -------------------------------
# For backward compatibility
# -------------------------------
def calculate_grade_and_gpa(score: float) -> Tuple[str, float]:
    """Return (letter grade, GPA points) tuple for a given score."""
    return get_letter_grade(score), get_grade_point(score)
