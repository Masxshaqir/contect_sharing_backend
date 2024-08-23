from django_filters import rest_framework as filters
from .models import Post
from django.db import models

class PostFilter(filters.FilterSet):
    # username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    popularity = filters.OrderingFilter(
        fields=(
            ('vote__count', 'popularity'),
        ),
        method='filter_popularity'
    )
    post_time = filters.DateFromToRangeFilter(field_name='post_time')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    content_keywords = filters.CharFilter(field_name='content', lookup_expr='icontains')
    hashtag = filters.CharFilter(field_name='hashtag', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = [ 'popularity', 'post_time', 'title', 'content_keywords','hashtag', 'category']

    def filter_popularity(self, queryset, name, value):
        return queryset.annotate(vote_count=models.Count('vote')).order_by('-vote_count')
