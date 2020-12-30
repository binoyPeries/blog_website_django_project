from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# dummy data
# posts = [
#     {
#         'author': 'jane doe',
#         'title': 'three little',
#         'content': 'first post',
#         'date_posted': '12/5/2020'
#     },
# ]

# this is used to do the rendering process of pages

# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     # template ref: sub directory within the temp/temp name
#     return render(request, 'blog/home.html', context)


# same procees can be done using a class based approach
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # the obj that we are passing to home template
    # if we explicitly dont define the  context_object_name it will bw by default object

    context_object_name = 'posts'
    # this is to sort the list
    ordering = ['-date_posted']
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post


# LoginRequiredMixin this willl stop from accessing crete post without getting logged in
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # since author is the current user we need to fill that field with the user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
