from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BookingViewSet, ListingViewSet, ReviewViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('listings', ListingViewSet)
router.register('bookings', BookingViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]