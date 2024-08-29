from django_filters import rest_framework as filters
from .models import Post
from django.db import models
from django.db.models import Q
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
    user_name = filters.CharFilter(method='filter_by_user_name')

    class Meta:
        model = Post
        fields = [ 'popularity', 'post_time', 'title', 'content_keywords','hashtag', 'category','user_name']

    def filter_by_user_name(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) | 
            Q(user__last_name__icontains=value)
        )
    def filter_popularity(self, queryset, name, value):
        return queryset.annotate(vote_count=models.Count('vote')).order_by('-vote_count')
