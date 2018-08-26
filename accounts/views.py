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
from jobs.models import Section, Gang, Position, Date

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
    application = get_object_or_404(Application, applicant_id=userID)
    applicant = application.applicant
    date, created = Date.objects.get_or_create(user=applicant)
    interviewers = [pos.interviewer for pos in application.get_positions()]
    userstatus = applicant.get_status()
    interview_time = application.get_interview_time()


    if request.method == 'POST':
        form = StatusForm(instance=applicant)
        chosen_time = request.POST.get('interviewtime') # Get the time marked in front-end
        chosen_room = request.POST.get('interviewroom') # Get the room chosen in front-end
        print('Chosen time: ' + str(chosen_time))
        print('Chosen room: ' + str(chosen_room))
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
            form.save()

    # GET or form failed:
    else:
        form = StatusForm(instance=applicant) # Ved å gi instance fyller den inn current status
        # TIPS: Lages det en tom StatusForm, kan Select-box settes til user current status slik:
        # form.fields['status'].initial = applicant.status

    interviewers_dir = {'kris@test.no': get_object_or_404(Date, user=User.objects.get(email='kris@test.no')).dates_list(),
     'camilla@test.no': get_object_or_404(Date, user=User.objects.get(email='camilla@test.no')).dates_list(),
      'johan@test.no': get_object_or_404(Date, user=User.objects.get(email='johan@test.no')).dates_list()}
    print(interviewers_dir['kris@test.no'])
    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
        'interviewers': interviewers,
        'interview_time': application.get_interview_time(),
        'interviewers_times': json.dumps(interviewers_dir)
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
