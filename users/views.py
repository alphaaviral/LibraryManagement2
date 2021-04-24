from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Profile
from books.models import request_detail

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created succesfully!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context={
        'form': form,
        'title': 'Sign Up',
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated succesfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'title': 'User Profile'
        }
        return render(request, 'users/profile.html', context)


def ProfileDetailView(request, **kwargs):
    user = User.objects.filter(id=kwargs['pk'])[0]
    requests = request_detail.objects.filter(requested_by=user)
    context = {
        'requests': requests,
        'user': user
    }
    return render(request, 'users/profile_for_lib.html', context)


class UserRequestsListView(LoginRequiredMixin, ListView):
    model = request_detail
    template_name = 'users/user_requests.html'
    context_object_name = 'requests'
    ordering = ['-date_added']

    def get_queryset(self):
        user = self.request.user
        return request_detail.objects.filter(requested_by=user)