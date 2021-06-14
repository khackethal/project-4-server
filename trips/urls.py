from django.urls import path
from .views import (
    TripListView,
    TripDetailView,
    TripLikeView,
    CommentListView,
    CommentDetailView
)

urlpatterns = [
    path('', TripListView.as_view()),
    path('<int:pk>/', TripDetailView.as_view()),
    path('<int:pk>/like/', TripLikeView.as_view()),
    path('<int:trip_pk>/comments/', CommentListView.as_view()),
    path('<int:_trip_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
]