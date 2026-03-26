from django.urls import path
from apps.user.views.authentications import RegisterView, LoginView, LogoutView
from apps.user.views.profiles import ChangePasswordView, MyProfileView, UserListView, UserAspirationRankingView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', MyProfileView.as_view(), name='my-profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('user/list/', UserListView.as_view(), name='user-list'),
    path('user/ranking/', UserAspirationRankingView.as_view(), name='user-ranking'),
]