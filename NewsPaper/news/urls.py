from django.urls import path
from django_filters.views import FilterView

from .models import Post
from .views import NewsList, NewsCopy, SearchNews, PostCreate, PostEdit, PostDelete


urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsCopy.as_view(), name='news_copy'),
   path('search', SearchNews.as_view(), name='news_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]