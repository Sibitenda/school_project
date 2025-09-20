# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Grade
from .forms import StudentForm, GradeForm

# ---- Student Views ----
def student_list(request):
    students = Student.objects.all()
    return render(request, "reports/student_list.html", {"students": students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = Grade.objects.filter(student=student)
    return render(request, "reports/student_detail.html", {"student": student, "grades": grades})

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "reports/student_form.html", {"form": form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, "reports/student_form.html", {"form": form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "reports/student_confirm_delete.html", {"student": student})


# ---- Grade Views ----
def grade_create(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student
            grade.save()
            return redirect("student_detail", pk=student.pk)
    else:
        form = GradeForm()
    return render(request, "reports/grade_form.html", {"form": form, "student": student})
