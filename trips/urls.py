from django.urls import path
from .views import (
    TripListView,
    TripDetailView,
    TripLikeView,
    CommentListView,
    CommentDetailView,
    UserTripListView,
    TripAddListView,
    UserTripListDetailView
)

urlpatterns = [
    path('', TripListView.as_view()),
    path('lists/',UserTripListView.as_view()),
    path('lists/<int:pk>/', UserTripListDetailView.as_view()),
    path('<int:pk>/', TripDetailView.as_view()),
    path('<int:list_pk>/list/<int:trip_pk>/', TripAddListView.as_view()),
    path('<int:pk>/like/', TripLikeView.as_view()),
    path('<int:trip_pk>/comments/', CommentListView.as_view()),
    path('<int:_trip_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
]