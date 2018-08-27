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
        # Get position or None
        #position = Position.objects.filter(contact_person=request.user).first()
        interviews = Interview.objects.filter(interviewers=request.user.pk)
        interview_list = list(interviews)
        all_interviewers = []
        me = []

        for i in interview_list:
            all_interviewers.append(i.interviewers.all())

        for j in range(all_interviewers.__len__()):
            for k in all_interviewers[j]:
                if k == request.user and me == []:
                    me.append(k)

        me_instance = None
        if me != []:
            me_instance = me[0]

        user = request.user
        user_gang_applications = Application.objects.filter(
            Q(first__gang=user.gang) | Q(second__gang=user.gang) | Q(third__gang=user.gang)
        )

        return render(request, 'accounts/profile_admin.html', {
            'me' : me_instance,
            'interviews' : interview_list,
            'user_gang_applications': user_gang_applications,
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
    application = get_object_or_404(Application, applicant_id=userID)
    applicant = application.applicant
    date, created = Date.objects.get_or_create(user=applicant)
    interviewers = [pos.contact_person for pos in application.get_positions()]
    userstatus = applicant.get_status()
    interview_time = application.get_interview_time()
    DATES_LENGTH = 182
    # BUG: Error if application doesn't have first or second positions. Possibly fixed

    # Find available times that match both applicant and interviewer(s)
    all_dates = application.applicant.date.dates_list()
    avail_times = [1] * DATES_LENGTH

    if len(application.get_positions()) >= 1:
        if application.first.contact_person != None:
            all_dates = all_dates + application.first.contact_person.date.dates_list()
        else:
            all_dates += all_dates
    if len(application.get_positions()) >= 2:
        if application.second.contact_person != None:
            all_dates = all_dates + application.second.contact_person.date.dates_list()
        else:
            all_dates += all_dates
        avail_times = [0] * DATES_LENGTH

    for i in range(len(all_dates)):
        avail_times[all_dates[i]] += 1
    if interview_time != 'none': # The time when the interview is set is also available
        avail_times[int(interview_time)] = 3
    # Available times found (reprecented as an array where the number 3 means an available time)

    if request.method == 'POST':
        form = StatusForm(instance=applicant)
        chosen_time = request.POST.get('interviewtime') # Get the time marked on front-end
        if not chosen_time: # If chosen_time never is submitted (i.e. user click on something else that refreshes the page)
            chosen_time = interview_time

        # Updating the interviewers availability
        if chosen_time != application.get_interview_time():
            for i in range(2):
                i = Date.objects.get(user=interviewers[i])
                if chosen_time != 'none': # If a new interview time is set
                    print(chosen_time)
                    i.remove_time(chosen_time)
                if application.get_interview_time() != 'none': # If there was no interview set in beforehand
                    i.add_time(interview_time)
                i.save()
                print("Available times for interviewer {} are updated".format(i.user.email))

            application.set_interview_time(chosen_time)
            application.save()
            print('Interview time changed to ' + chosen_time)

        print('request.POST, instance=applicant')
        form = StatusForm(request.POST, instance=applicant)

        if form.is_valid():
            print('form valid')
            form.save() # Lagrer status direkte på user fordi instance er gitt
            # TIPS: Kan droppe form.save() for å endre objekt manuelt med form-data. men HUSK: save objektet etterpå
            # Example:
                #applicant.status = form.cleaned_data.get('status')
                #applicant.save()

    # GET or form failed:
    else:
        form = StatusForm(instance=applicant) # Ved å gi instance fyller den inn current status
        # TIPS: Lages det en tom StatusForm, kan Select-box settes til user current status slik:
        # form.fields['status'].initial = applicant.status
    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
        'interviewers': interviewers,
        'avail_times': avail_times,
        'interview_time': application.get_interview_time()
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
