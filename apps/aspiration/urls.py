from django.urls import path
from apps.aspiration.views import CategoryListView, AspirationListCreateView, AspirationDetailView, AspirationProgressListCreateView, NotificationListView, NotificationReadView    

urlpatterns = [
    path('aspiration/categories/', CategoryListView.as_view(), name='category-list'),
    path('aspiration/list/', AspirationListCreateView.as_view(), name='aspiration-list'),
    path('aspiration/list/<uuid:pk>/', AspirationDetailView.as_view(), name='aspiration-detail'),
    path('aspiration/progress/', AspirationProgressListCreateView.as_view(), name='progress-create'),
    path('aspiration/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('aspiration/notifications/<uuid:pk>/read/', NotificationReadView.as_view(), name='notification-read'),
]