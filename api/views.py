from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F, ExpressionWrapper, fields, Case, When, QuerySet
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import User, Hobby, FriendRequest
from .serializers import UserSerializer, HobbySerializer, FriendSerializer, UserReadSerializer
import json
import logging
from django.middleware.csrf import get_token
from rest_framework.generics import ListAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from datetime import date
from typing import Any, Dict




logger = logging.getLogger(__name__)

def get_csrf_token(request) -> JsonResponse:
    token = get_token(request)
    return JsonResponse({'token': token})

# Main SPA View
@login_required
def main_spa(request) -> HttpResponse:
    return render(request, 'static/api/spa/index.html')

# Login View
@csrf_protect
def login_view(request) -> JsonResponse:
    if request.method == 'POST':
        try:
            data: Dict[str, Any] = json.loads(request.body)
            email: str = data.get('email')
            password: str = data.get('password')

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'error': 'GET method not allowed'}, status=405)

# Logout View
def logout_view(request) -> JsonResponse:
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

# Friend Request
class ListFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> QuerySet:
        user = self.request.user
        return FriendRequest.objects.filter(Q(receiver=user) )
    
    def get_object(self) -> FriendRequest:
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, self.kwargs.get('pk'))
        return obj
    
class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> QuerySet:
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) )
    
class addFriendRequestView(generics.ListCreateAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> QuerySet:
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user))
    
class UpdateFriendRequestsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user))
    
    def get_object(self) -> FriendRequest:
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj
    
#Friends Request Action
class FriendRequestActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest, action: str) -> Response:
        try:
            friend_request_id: int = request.data.get('friend_request_id')
            friend_request: FriendRequest = FriendRequest.objects.get(id=friend_request_id)

            if action == 'accept':
                friend_request.accept()
            elif action == 'reject':
                friend_request.reject()
            elif action == 'cancel':
                friend_request.cancel()
            else:
                return Response({'error': 'Invalid action'}, status=400)
            
            return Response({'message': f'Friend request {action}ed succesfully'})
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=404)
        except Exception as e:
            logger.error(f"Friend request action error: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=500)
        
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return UserReadSerializer
        return UserSerializer

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
        serializer = UserReadSerializer(users, many=True)
        return Response(serializer.data)
    
class SimilarUsersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # Allow clients to override page size
    max_page_size = 50  # Maximum allowed page size

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,  # Total number of items
            'results': data  # Current page data
        })

@api_view(['GET'])
def similar_users(request):
    user: User = request.user
    user_hobbies: QuerySet = user.hobbies.values_list('id', flat=True)
    today: date = date.today()


    calculated_age = ExpressionWrapper(
        today.year - F('date_of_birth__year') -
        Case(
            When(
                Q(date_of_birth__month__gt=today.month) |
                Q(date_of_birth__month=today.month, date_of_birth__day__gt=today.day),
                then=1
            ),
            default=0,
            output_field=fields.IntegerField()
        ),
        output_field=fields.IntegerField()
    )


    min_age: int = int(request.query_params.get('min_age', 0))
    max_age: int = int(request.query_params.get('max_age', 100))


    similar_users: QuerySet = (
        User.objects.exclude(id=user.id)
        .annotate(
            similarity_score=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies)),
            calculated_age=calculated_age
        )
        .filter(calculated_age__gte=min_age, calculated_age__lte=max_age)
        .order_by('-similarity_score')
    )

    paginator = SimilarUsersPagination()
    result_page = paginator.paginate_queryset(similar_users,request)
    serializer = UserReadSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)    
