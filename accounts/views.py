from django.shortcuts import render, redirect, get_object_or_404
#from django.views import generic
#from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.forms import SignUpForm, StatusForm
from accounts.models import User
from applications.models import Application
from jobs.models import *

# Create your views here.
@login_required
def profile(request):
    application = Application.objects.filter(applicant=request.user).first()
    positions = None
    if application != None:
        positions = application.get_positions()

    return render(request, 'accounts/profile.html', {
        'positions':positions},
    )

# BUG: Oppdateres siden med get request får man error
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
        # So that error messages are not displayed at the first try
        elif form.cleaned_data.get('first_name') == None:
            form = SignUpForm()

        return render(request, 'accounts/registration_form.html', {'form':form})


def logout_view(request):
    print("==================================================")
    logout(request)
    # Redirect to a success page.
    render(request, 'accounts/logout.html')

def manage_profile(request, user_id):
    application = get_object_or_404(Application, applicant_id=user_id)
    user = get_object_or_404(User, id=user_id)
    dates = Date.objects.get_or_create(user=request.user)
    form = StatusForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user.status = form.cleaned_data.get('menu')
            user.save()

    #stat = User.objects.get('status')
    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'dates': dates,
        'form': form,
    })
