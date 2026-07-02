"""
Views for the Accounts app.

Handles: Registration, Login, Logout, and Profile pages.
Login/Logout use Django's built-in auth views (configured in urls.py),
so this file only needs to handle Register and Profile.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileUpdateForm


def register(request):
    """
    Handles new user registration.
    On success, logs the user in automatically and redirects to the home page.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to TastyBite, {user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """
    Displays and allows editing of the logged-in user's profile information.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})