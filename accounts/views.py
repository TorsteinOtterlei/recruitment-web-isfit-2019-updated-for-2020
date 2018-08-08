from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# local:
from accounts.forms import SignUpForm, StatusForm, WidgetsForm
from accounts.models import User
# other apps:
from applications.models import Application
from jobs.models import Section, Gang, Position, Date

# Create your views here.
@login_required
def profile(request):
    if request.user.is_staff:
        return render(request, 'accounts/profile_admin.html')
        
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

@staff_member_required
def manage_profile(request, userID):
    application = get_object_or_404(Application, applicant_id=userID)
    applicant = application.applicant
    date, created = Date.objects.get_or_create(user=applicant)
    interviewers = [pos.interviewer for pos in application.get_positions()]
    if applicant.email == "emil.telstad@live.no":
        #pass
        applicant.email_user(subject="Test", message="My msg", from_email="emilte@stud.ntnu.no")

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data.get('status'))
            applicant.status = form.cleaned_data.get('status')
            applicant.save()
    else:
        form = StatusForm()
        form.fields['status'].initial = applicant.status
    #stat = User.objects.get('status')
    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
        'interviewers': interviewers,
    })

def widgets(request):
    form = WidgetsForm()
    return render(request, 'accounts/widgets.html', {'form': form})
