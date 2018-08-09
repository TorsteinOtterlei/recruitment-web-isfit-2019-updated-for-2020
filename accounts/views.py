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
    print(request.user)
    if request.user.is_staff:
        return render(request, 'accounts/profile_admin.html')

    application = Application.objects.filter(applicant=request.user).first()
    positions = None
    if application != None:
        positions = application.get_positions()

    return render(request, 'accounts/profile.html', {
        'positions':positions},
    )

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            print("{} has registered in!".format(user))
            return redirect('home')
    # GET or form failed:
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
    userstatus = applicant.get_status()

    DATES_LENGTH = 140
    all_dates = application.applicant.date.dates_list() + \
                application.first.interviewer.date.dates_list() + \
                application.second.interviewer.date.dates_list()
    avail_times = [0] * DATES_LENGTH
    for i in range(len(all_dates)):
        avail_times[all_dates[i]] += 1
    #if applicant.email == "emil.telstad@live.no":
        #pass
        #applicant.email_user(subject="Test", message="My msg", from_email="emilte@stud.ntnu.no")

    if request.method == 'POST':
        form = StatusForm(instance=applicant)
        chosen_time = request.POST.get('interviewtime')

        if userstatus == 'NE': # It is not possible to manually change from NE to IS
            if chosen_time != None:
                print('ne')
                # TODO: make interviewers busy
                # TODO: set appliaction interview date (also using this in front-end to mark chosen-time)
                applicant.status = 'IS'
                applicant.save() # Changing from NE to IS automatic when an interview is set
                form = StatusForm(instance=applicant)

        elif userstatus in ['IS', 'IC', 'ID', 'AC']: #TODO: More restrictions, what should
                                                     # be automatic and what should be changed manually ?
            form = StatusForm(request.POST, instance=applicant)

            if form.is_valid():
                # if (form.cleaned_data['status'] == 'NE'):
                #     # TODO: Handle removing/changing interview

                form.save() # Lagrer status direkte på user fordi instance er gitt
                # Kan droppe form.save() for å endre objekt manuelt med form-data. men HUSK: save objektet etterpå
                # Example:
                    #applicant.status = form.cleaned_data.get('status')
                    #applicant.save()
    else:
        form = StatusForm(instance=applicant) # Ved å gi instance fyller den inn current status
        # Lages det en tom StatusForm, kan Select-box settes til user current status slik:
            #form.fields['status'].initial = applicant.status
    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
        'interviewers': interviewers,
        'avail_times': avail_times
    })

def widgets(request):
    form = WidgetsForm()
    return render(request, 'accounts/widgets.html', {'form': form})
