from django.shortcuts import render
from .models import User, Listing, Booking, Review
from .serializers import UserSerializer, ListingSerializer, BookingSerializer, ReviewSerializer, CustomAuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# Create your views here.

class IsAuthenticatedAndGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_guest

class IsAuthenticatedAndHost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_host

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedAndHost]
    
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
        
    def get_queryset(self):
        # hosts see their own listings
        return self.queryset.filter(host=self.request.user)
        
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedAndGuest]
    
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)
        
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedAndGuest]
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
        
    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})