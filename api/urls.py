from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import (
    main_spa,
    login_view,
    logout_view,
    RegisterUserView,
    UserProfileView,
    HobbyListCreateView,
    AllUsersView,
    similar_users,
    get_csrf_token,
    ListFriendRequestsView,
    UpdateFriendRequestsView,
    addFriendRequestView,
    ListPendingRequestsView
)

spa = login_required(main_spa)

urlpatterns = [
    path('', spa, name='home'),  # Ensures login required for the main SPA
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', login_view, name='login'), 
    path('logout/', logout_view, name='logout'),  # Using Django's built-in logout view
    path('profile/', login_required(UserProfileView.as_view()), name='profile'),  # Securing profile route
    path('hobbies/', login_required(HobbyListCreateView.as_view()), name='hobby-list'),  # Securing hobbies route
    path('api/users/', AllUsersView.as_view(), name='all-users'),
    path('similar-users/', similar_users, name='similar-users'),
    path('get-token/', get_csrf_token, name='getToken'),
    path('api/getPendingRequests/', ListPendingRequestsView.as_view(), name='listPendingRequests'),
    path('api/friend-requests/<int:pk>/', UpdateFriendRequestsView.as_view()),
    path('api/friend-requests/', ListFriendRequestsView.as_view(), name='friend-request'),
    path('api/addFriendRequest/', addFriendRequestView.as_view(), name='addFriendRequest'),
]
