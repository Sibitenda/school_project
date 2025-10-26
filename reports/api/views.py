from rest_framework import viewsets, permissions
from .serializers import (
    ProfileSerializer, CourseSerializer, StudentMarkSerializer,
    AchievementSerializer, SupportTicketSerializer,
    CareerOpportunitySerializer, StudentDashboardSerializer
)
from reports.models import (
    Profile, Course, StudentMark, Achievement,
    SupportTicket, CareerOpportunity
)
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reports.models import Profile, Course, StudentMark, Achievement, SupportTicket
from reports.utils.grade_utils import calculate_gpa, calculate_cpa

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all().select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.select_related('lecturer').prefetch_related('students')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StudentMarkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentMark.objects.select_related('student', 'course', 'lecturer')
    serializer_class = StudentMarkSerializer
    permission_classes = [permissions.IsAuthenticated]

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SupportTicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SupportTicket.objects.select_related('student')
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

class CareerOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CareerOpportunity.objects.all()
    serializer_class = CareerOpportunitySerializer
    permission_classes = [permissions.AllowAny]

# Student dashboard (aggregated)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Return JSON dashboard data (for mobile app)."""
        user = request.user
        profile = getattr(user, "profile", None)

        # Admin dashboard summary
        if profile and profile.role == "admin":
            data = {
                "profile": {"name": user.username, "role": "Admin"},
                "summary": {
                    "students": Profile.objects.filter(role="student").count(),
                    "lecturers": Profile.objects.filter(role="lecturer").count(),
                    "courses": Course.objects.count(),
                    "marks": StudentMark.objects.count(),
                    "achievements": Achievement.objects.count(),
                    "tickets": SupportTicket.objects.count(),
                },
            }
            return Response(data)

        # Student dashboard details
        elif profile and profile.role == "student":
            marks = StudentMark.objects.filter(student=profile)
            gpa = calculate_gpa(marks)
            cpa = calculate_cpa(profile)
            data = {
                "profile": {"name": profile.name, "role": "Student"},
                "gpa": gpa,
                "cpa": cpa,
                "marks": [
                    {
                        "course": m.course.name,
                        "score": m.score,
                        "grade": m.grade,
                        "gpa": m.gpa,
                    }
                    for m in marks
                ],
            }
            return Response(data)

        # Default fallback
        return Response({"profile": {"name": user.username, "role": "Unknown"}})

