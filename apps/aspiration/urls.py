from django.urls import path
from apps.aspiration.views.aspirations import AspirationHistoryListView, AspirationStatsView, AspirationUpdateDestroyView, AspirationProgressDetailUpdateDestroyView, AspirationListCreateView, AspirationDetailView, AspirationProgressListCreateView, AspirationCategoryStatsView
from apps.aspiration.views.categories import CategoryListView, CategoryCreateView, CategoryDetailUpdateDestroyView
from apps.aspiration.views.locations import LocationListView, LocationCreateView, LocationDetailUpdateDestroyView
from apps.aspiration.views.notifications import NotificationListView, NotificationReadAllView, NotificationReadView, NotificationDetailDestroyView    
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('aspiration/categories/', CategoryListView.as_view(), name='category-list'),
    path('aspiration/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('aspiration/categories/<uuid:pk>/manage/', CategoryDetailUpdateDestroyView.as_view(), name='category-manage'),

    path('aspiration/locations/', LocationListView.as_view(), name='location-list'),
    path('aspiration/locations/create/', LocationCreateView.as_view(), name='location-create'),
    path('aspiration/locations/<uuid:pk>/manage/', LocationDetailUpdateDestroyView.as_view(), name='location-manage'),
    
    path('aspiration/list/', AspirationListCreateView.as_view(), name='aspiration-list-create'),
    path('aspiration/list/<uuid:pk>/', AspirationDetailView.as_view(), name='aspiration-detail'),
    path('aspiration/list/<uuid:pk>/manage/', AspirationUpdateDestroyView.as_view(), name='aspiration-manage'),
    path('aspiration/progress/', AspirationProgressListCreateView.as_view(), name='progress-list-create'),
    path('aspiration/progress/<uuid:pk>/manage/', AspirationProgressDetailUpdateDestroyView.as_view(), name='progress-detail-manage'),
    path('aspiration/stats/', AspirationStatsView.as_view(), name='aspiration-stats'),
    path('aspiration/category-stats/', AspirationCategoryStatsView.as_view(), name='aspiration-category-stats'),
    path('aspiration/history/', AspirationHistoryListView.as_view(), name='aspiration-history'),
    
    path('aspiration/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('aspiration/notifications/<uuid:pk>/read/', NotificationReadView.as_view(), name='notification-read'),
    path('aspiration/notifications/all-read/', csrf_exempt(NotificationReadAllView.as_view()), name='notification-all-read'),
    path('aspiration/notifications/<uuid:pk>/manage/', NotificationDetailDestroyView.as_view(), name='notification-manage'),
]