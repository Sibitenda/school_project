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
from rest_framework.decorators import action
from rest_framework.response import Response

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def student(self, request):
        profile = getattr(request.user, "profile", None)
        if not profile:
            return Response({"error": "Profile not found"}, status=404)
        serializer = StudentDashboardSerializer(profile)
        return Response(serializer.data)
