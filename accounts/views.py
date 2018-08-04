from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# local:
from accounts.forms import SignUpForm, StatusForm
from accounts.models import User
# other apps:
from applications.models import Application
from jobs.models import Section, Gang, Position, Date

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

def manage_profile(request, userID):
    application = get_object_or_404(Application, applicant_id=userID)
    date, created = Date.objects.get_or_create(user_id=userID)
    form = StatusForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = get_object_or_404(User, id=userID)
            user.status = form.cleaned_data.get('menu')
            user.save()
            form.save()
    #stat = User.objects.get('status')
    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
    })
