from django.urls import path
from apps.aspiration.views.aspirations import AspirationStatsView, AspirationUpdateDestroyView, AspirationProgressDetailUpdateDestroyView, AspirationListCreateView, AspirationDetailView, AspirationProgressListCreateView
from apps.aspiration.views.categories import CategoryListView, CategoryCreateView, CategoryDetailUpdateDestroyView
from apps.aspiration.views.notifications import NotificationListView, NotificationReadView, NotificationDetailDestroyView    

urlpatterns = [
    path('aspiration/categories/', CategoryListView.as_view(), name='category-list'),
    path('aspiration/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('aspiration/categories/<uuid:pk>/manage/', CategoryDetailUpdateDestroyView.as_view(), name='category-manage'),
    
    path('aspiration/list/', AspirationListCreateView.as_view(), name='aspiration-list-create'),
    path('aspiration/list/<uuid:pk>/', AspirationDetailView.as_view(), name='aspiration-detail'),
    path('aspiration/list/<uuid:pk>/manage/', AspirationUpdateDestroyView.as_view(), name='aspiration-manage'),
    path('aspiration/progress/', AspirationProgressListCreateView.as_view(), name='progress-list-create'),
    path('aspiration/progress/<uuid:pk>/manage/', AspirationProgressDetailUpdateDestroyView.as_view(), name='progress-detail-manage'),
    path('aspiration/stats/', AspirationStatsView.as_view(), name='aspiration-stats'),
    
    path('aspiration/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('aspiration/notifications/<uuid:pk>/read/', NotificationReadView.as_view(), name='notification-read'),
    path('aspiration/notifications/<uuid:pk>/manage/', NotificationDetailDestroyView.as_view(), name='notification-manage'),
]