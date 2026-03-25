import django_filters
from apps.aspiration.models import Aspiration
from apps.user.models import CoreStudent 

class AspirationFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    category = django_filters.CharFilter(field_name='category_id', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    
    user = django_filters.CharFilter(
        field_name='user__id',
        lookup_expr='exact'
    )

    class Meta:
        model = Aspiration
        fields = ['start_date', 'end_date', 'category', 'status', 'user']