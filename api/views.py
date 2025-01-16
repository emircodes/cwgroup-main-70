from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User, Hobby, FriendRequest
from .serializers import UserSerializer, HobbySerializer, FriendSerializer
import json
import logging
from django.middleware.csrf import get_token
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView



logger = logging.getLogger(__name__)

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token})

# Main SPA View
@login_required
def main_spa(request):
    return render(request, 'templates/api/spa/index.html')

# Login View
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

# Logout View
def logout_view(request):
    logout(request)

# Friend Request
class ListFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(receiver=user))
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, self.kwargs.get('pk'))
        return obj
    
class addFriendRequestView(generics.ListCreateAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user))
    
class UpdateFriendRequestsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user))
    

    
             
        
# Register User View
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Registration should be open to everyone

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f"Registration errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return Response({"error": "Something went wrong on the server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Profile View
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Returns the authenticated user
    
    

# Hobby List/Create View
class HobbyListCreateView(generics.ListCreateAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
    permission_classes = [IsAuthenticated]

class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def similar_users(request):
    # Get the hobbies of the current user
    user = request.user
    user_hobbies = user.hobbies.all()

    # Get other users and count similar hobbies
    similar_users = (
        User.objects.exclude(id=user.id)  # Exclude the current user
        .annotate(similarity_score=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies)))  # Use Q for filtering
        .order_by('-similarity_score')  # Order by similarity score
    )

    serializer = UserSerializer(similar_users, many=True)
    return Response(serializer.data)
