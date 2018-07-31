from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
from applications.models import Application

# Create your views here.
@login_required
def profile(request):
    positions = None

    print(Application.objects.filter(applicant=request.user).first())
    if Application.objects.filter(applicant=request.user).first():
        user_application = Application.objects.filter(applicant=request.user).first()

        positions = [user_application.first]

        if user_application.second is not None:
            positions.append(user_application.second)
            if user_application.second is not None:
                positions.append(user_application.third)

    return render(request, 'accounts/profile.html', {
        'positions':positions,
    })

# BUG: Oppdateres siden med get request får man error
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'accounts/registration_form.html', {'form':form})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    render(request, 'accounts/logout.html')
