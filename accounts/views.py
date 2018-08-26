from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.db.models import Q
import json
# local:
from accounts.forms import SignUpForm, StatusForm, WidgetsForm, CustomAuthenticationForm
from accounts.models import User
# other apps:
from applications.models import Application
from jobs.models import Section, Gang, Position, Date, Interview

@login_required
def profile(request):
    print(request.user)
    # Admin profile should look different
    if request.user.is_staff:
        # Default: this staff/interviewer has no position, thus no applications applied for it
        applications = []
        IS_applications = []
        # Get position or None
        position = Position.objects.filter(interviewer=request.user).first()
            # Check if user is an interviewer
        if position != None:
            IS_applications = Application.objects.filter(
                        ~Q(interview_time=-1),
                        Q(first=position) | Q(second=position)
                    ).order_by('interview_time')
            applications = Application.objects.all()
        return render(request, 'accounts/profile_admin.html', {
            'IS_applications': IS_applications,
            'applications': applications,
        })
    # Normal profile
    application = Application.objects.filter(applicant=request.user).first()
    positions = []
    if application != None:
        positions = application.get_positions()
    return render(request, 'accounts/profile.html', {
        'positions': positions,
    })

def signup(request):
    if request.method == "GET":
        form = SignUpForm() # GET should give a new form
    else: # POST
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            print("{} has registered!".format(user))
            return redirect('home')

    # GET or form failed. Form is either empty or contains previous POST with errors:
    return render(request, 'accounts/registration_form.html', {'form':form})


# NOTE: Not in use
def logout_view(request):
    print("==================================================")
    logout(request)
    # Redirect to a success page.
    render(request, 'accounts/logout.html')

@staff_member_required
def manage_profile(request, userID):
    # ----------------------------------------------------------------------------------------
    # TODO CHANGE INTERVIEW TO FIRST SECOND THIRD!
    # ----------------------------------------------------------------------------------------
    application = get_object_or_404(Application, applicant_id=userID)
    positions = application.get_positions()
    if len(positions) == 1:
        positions = positions * 2
    applicant = application.applicant
    date, created = Date.objects.get_or_create(user=applicant)
    userstatus = applicant.get_status()

    if request.method == 'POST':
        interview, interview_created = Interview.objects.get_or_create(applicant=application.applicant)
        form = StatusForm(instance=applicant)
        chosen_time = request.POST.get('interviewtime') # Get the time marked in front-end
        chosen_room = request.POST.get('interviewroom') # Get the room chosen in front-end
        chosen_interviewers = []
        for inter in request.POST.get('interviewers').split(','):
            if inter != 'None':
                chosen_interviewers.append(User.objects.get(email=inter))
        print('Chosen time: ' + str(chosen_time))
        print('Chosen room: ' + str(chosen_room))
        print('Chosen interviewers: ' + str(chosen_interviewers))


        # Updating the interviewers availability
        if chosen_time != application.get_interview_time():
             # Remove old unavailable times
            for inter in interview.interviewers.all():
                userdate = Date.objects.get(user=inter)
                userdate.add_time(application.get_interview_time())
                userdate.save()
             # Add new unavailable times
            for inter in chosen_interviewers:
                userdate = Date.objects.get(user=inter)
                userdate.remove_time(chosen_time)
                userdate.save()

            application.set_interview_time(chosen_time)
            application.save()
            print('Interview time changed to ' + str(chosen_time))

        # Update/create interview object
        interview.interviewers.add(*chosen_interviewers)
        interview.room = chosen_room
        interview.set_interview_time(chosen_time)
        interview.save()
        print('Created interview object!') if interview_created else print('Updated interview object!')

        print('request.POST, instance=applicant')
        form = StatusForm(request.POST, instance=applicant)

        if form.is_valid():
            print('form valid')
            form.save()

    # GET or form failed:
    else:
        form = StatusForm(instance=applicant)

    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
        'positions': positions
    })

def send_mail(request, userID):
    emil, created = User.objects.get_or_create(email="twidex97@gmail.com")
    user = get_object_or_404(User, id=userID)

    msg = """You have got an interview with ISFiT
            Your interview is {}
            Interviewer: {}

            Sent from {}""".format(user.application.pretty_date(), user.application.first, request.user)

    emil.email_user(subject="Interview", message=msg, from_email="emil.telstad@live.no")
    user.email_user(subject="Interview", message=msg, from_email=request.user.email)
    return HttpResponse()
    #return manage_profile(request, userID)

def widgets(request):
    form = WidgetsForm()
    return render(request, 'accounts/widgets.html', {'form': form})
