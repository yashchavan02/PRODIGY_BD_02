from django.urls import path
from app.views import UserListAPIView, UserDetailAPIView

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<str:id>/', UserDetailAPIView.as_view(), name='user-detail'),
]
