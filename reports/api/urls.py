from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet, CourseViewSet, StudentMarkViewSet,
    AchievementViewSet, SupportTicketViewSet,
    CareerOpportunityViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'marks', StudentMarkViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'tickets', SupportTicketViewSet)
router.register(r'opportunities', CareerOpportunityViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls
