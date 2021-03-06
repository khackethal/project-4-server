from django.urls import path
from .views import RegisterView, LoginView, ProfileView, EditProfileView, EditProfileImageView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>', ProfileView.as_view()),
    path('profile/<int:pk>/edit/', EditProfileView.as_view()),
    path('profile/<int:pk>/edit/image/', EditProfileImageView.as_view()),
]