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
)

spa = login_required(main_spa)

urlpatterns = [
    path('', login_required(main_spa), name='home'),  # Ensures login required for the main SPA
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Using Django's built-in login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Using Django's built-in logout view
    path('profile/', login_required(UserProfileView.as_view()), name='profile'),  # Securing profile route
    path('hobbies/', login_required(HobbyListCreateView.as_view()), name='hobby-list'),  # Securing hobbies route
]
