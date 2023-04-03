from django.forms import DateTimeInput, Select
from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    postcategory = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория поста',

    )

    title_filter = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Содержит в названии'
    )

    date_after = DateTimeFilter(
        field_name='createDate',
        lookup_expr='gt',
        label='Начиная с даты',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'categoryType': ['exact'],
        }
