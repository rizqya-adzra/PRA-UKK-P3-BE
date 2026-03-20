import django_filters
from apps.aspiration.models import Aspiration

class AspirationFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    category = django_filters.CharFilter(field_name='category_id', lookup_expr='exact')
    
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Aspiration
        fields = ['start_date', 'end_date', 'category', 'status']