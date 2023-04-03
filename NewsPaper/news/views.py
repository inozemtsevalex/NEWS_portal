from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .models import Post, Author
from datetime import datetime
from .forms import PostForm
from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    ordering = '-createDate'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsCopy(DetailView):
    model = Post
    template_name = 'news_copy.html'
    context_object_name = 'news_copy'


class SearchNews(ListView):
    model = Post
    ordering = '-createDate'
    template_name = 'news_search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post_inst = form.save(commit=False)
        post_inst.author = self.request.user.author
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
