from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# local:
from accounts.forms import SignUpForm, StatusForm, WidgetsForm, CustomAuthenticationForm
from accounts.models import User
# other apps:
from applications.models import Application
from jobs.models import Section, Gang, Position, Date

@login_required
def profile(request):
    print(request.user)
    # Admin profile should look different
    if request.user.is_staff:
        return render(request, 'accounts/profile_admin.html')
    # Normal profile
    application, created = Application.objects.get_or_create(applicant=request.user)
    return render(request, 'accounts/profile.html', {
        'positions': application.get_positions(),
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
    interviewers = [pos.interviewer for pos in application.get_positions()]
    userstatus = applicant.get_status()
    interview_time = application.interview_time

    DATES_LENGTH = 140
    # BUG: Error if application doesn't have first or second positions. Possibly fixed

    # Find available times that match both applicant and interview(ers)
    all_dates = application.applicant.date.dates_list()
    avail_times = [1] * DATES_LENGTH

    if len(application.get_positions()) >= 1:
        all_dates = all_dates + application.first.interviewer.date.dates_list()
    if len(application.get_positions()) >= 2:
        all_dates = all_dates + application.second.interviewer.date.dates_list()
        avail_times = [0] * DATES_LENGTH

    for i in range(len(all_dates)):
        avail_times[all_dates[i]] += 1
    # Available times found (reprecented as an array where the number 3 means an available time)

    if request.method == 'POST':
        form = StatusForm(instance=applicant)
        chosen_time = request.POST.get('interviewtime') # Get the time marked on front-end
        if not chosen_time: # quickfix
            chosen_time = 'none'

        # Updating the interviewers availability
        if chosen_time != application.interview_time:
            for i in range(2):
                i = Date.objects.get(user=interviewers[i])
                if chosen_time != 'none':
                    i.remove_time(chosen_time)
                if application.interview_time != 'none':
                    i.dates += ',' + interview_time
                i.save()
                print("Available times for interviewer %s are updated" %(i.user.email))

        application.interview_time = chosen_time
        application.save()
        print('Interview time changed to ' + chosen_time)


        form = StatusForm(request.POST, instance=applicant)

        if form.is_valid():
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
        'interview_time': application.interview_time
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
