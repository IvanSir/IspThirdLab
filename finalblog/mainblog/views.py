from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from mainblog.forms import PostCreateForm, PostUpdateForm
from mainblog.models import Post


class HomeView(ListView):
    model = Post
    template_name = 'home.html'


def create_post(request):
    if request.user.is_authenticated:
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
    return redirect('login')


class DetailPostView(DetailView):
    model = Post
    template_name = 'post/detail.html'


def delete_post(request, slug):
    if request.method != 'POST' or Post.objects.filter(author=request.user, slug=slug) is None:
        raise Http404("No permission")
    Post.objects.filter(slug=slug).delete()
    return redirect('home')


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'post/update.html'
    fields = ('title', 'text')

    def get_object(self, queryset=None):
        obj = super(UpdatePostView, self).get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("No permission")
        return obj
