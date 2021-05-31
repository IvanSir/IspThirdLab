import profile

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from mainblog.models import Post, Role
from .forms import UserRegistrationForm

# Create your views here.
from .models import Account


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'home.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': user_form})


def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user is None:
                raise Exception
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        except:
            return render(request, 'users/login.html', {})
    else:
        return render(request, 'users/login.html', {})


def my_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        us_id = self.request.path.split('/')[2]
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=us_id)
        context['posts'] = Post.objects.select_related("author").filter(author_id=us_id)
        context['roles'] = Role.objects.prefetch_related("users").filter(users=context['user'])
        context['account'] = Account.objects.select_related("user").get(user_id=us_id)
        return context


def update_account(request, pk):
    if str(request.user.pk) != pk:
        return redirect('home')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        user = User.objects.get(id=pk)
        try:
            if phone is None:
                raise Exception
            if Account.objects.get(user=user) is not None:
                Account.objects.update(user=user, phone=phone)
            else:
                Account.objects.create(user=user, phone=phone)
            return redirect('detail_user', pk)
        except:
            return render(request, 'users/edit.html', {})
    else:
        return render(request, 'users/edit.html', {})
