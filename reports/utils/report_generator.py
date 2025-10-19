import asyncio
from typing import Dict, List
from .calculations import average
import matplotlib.pyplot as plt
import io
import base64
from typing import List


async def fetch_marks(marks_queryset) -> List:
    """
    Asynchronously fetch all student marks from the database.
    Uses Django's async queryset evaluation if supported (Django 4.1+).
    """
    # Convert to list asynchronously if supported
    if hasattr(marks_queryset, "aall"):
        marks = [m async for m in marks_queryset]
    else:
        # Fallback for sync ORM
        loop = asyncio.get_event_loop()
        marks = await loop.run_in_executor(None, list, marks_queryset)
    return marks


async def compute_student_summary_async(marks_queryset) -> Dict[str, float]:
    """
    Async version of compute_student_summary:
     - fetches queryset asynchronously
     - computes average concurrently
    """
    marks = await fetch_marks(marks_queryset)
    total = len(marks)
    if total == 0:
        return {"total_courses": 0, "average_gpa": 0.0}

    # Extract valid GPAs concurrently
    loop = asyncio.get_event_loop()
    gpas = await loop.run_in_executor(None, lambda: [m.gpa for m in marks if getattr(m, "gpa", None) is not None])

    avg_gpa = round(average(gpas), 2) if gpas else 0.0
    return {"total_courses": total, "average_gpa": avg_gpa}


def compute_student_summary(marks_queryset) -> Dict[str, float]:
    """
    Wrapper that auto-detects async context.
    If running in an async view, await it directly.
    Otherwise, runs event loop internally for compatibility.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Running inside async context
        return asyncio.ensure_future(compute_student_summary_async(marks_queryset))
    else:
        # Run standalone
        return asyncio.run(compute_student_summary_async(marks_queryset))

async def generate_report_chart(gpas: List[float]) -> str:
    
    """
    Generate a GPA distribution chart and return as base64 string for embedding in HTML.
    """
    plt.figure(figsize=(6, 4))
    plt.hist(gpas, bins=5, color='skyblue', edgecolor='black')
    plt.title('GPA Distribution')
    plt.xlabel('GPA')
    plt.ylabel('Number of Students')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return image_base64