import django_filters
from .models import Movies

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.BooleanFilter(label='Watched')
    class Meta:
        model = Movies
        fields = '__all__'
        exclude = ['user']

