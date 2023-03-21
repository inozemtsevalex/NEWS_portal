
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'createDate'
    template_name = 'news_list.html'
    context_object_name = 'news'


class NewsCopy(DetailView):
    model = Post
    template_name = 'news_copy.html'
    context_object_name = 'news_copy'
