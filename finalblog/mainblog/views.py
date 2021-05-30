from django.shortcuts import render, redirect

# Create your views here.
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, DetailView

from mainblog.forms import PostCreateForm
from mainblog.models import Post


class HomeView(ListView):
    model = Post
    template_name = 'home.html'


def create_post(request):
    if request.method == 'POST':
        post_form = PostCreateForm(request.POST)
        if post_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_post = post_form.save(commit=False)
            # Set the chosen password
            new_post.author = request.user
            # Save the User object
            new_post.save()
            return redirect('home')
    else:
        post_form = PostCreateForm()
    return render(request, 'post/create.html', {'form': post_form})


class DetailPostView(DetailView):
    model = Post
    template_name = 'post/detail.html'
