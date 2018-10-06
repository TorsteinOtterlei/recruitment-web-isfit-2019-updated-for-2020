from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.db.models import Q
from django.urls import reverse
import json
# local:
from accounts.forms import SignUpForm, StatusForm, RestrictedStatusForm, WidgetsForm, CustomAuthenticationForm, EditUserForm, CustomPasswordChangeForm
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

        # Getting interview objects where user is one of the interviewers
        unsorted_interviews = Interview.objects.filter(interviewers=request.user.pk).all()

        interviews = sorted(unsorted_interviews, key = lambda inter : inter.get_order_time())

        # interview_list = list(interviews)
        # all_interviewers = []
        # me = []
        #
        # for i in interview_list:
        #     all_interviewers.append(i.interviewers.all())
        #
        # # Finding self.user from list of all interviewers and appending on me
        # for j in range(all_interviewers.__len__()):
        #     for k in all_interviewers[j]:
        #         if k == request.user and me == []:
        #             me.append(k)
        #
        # # Getting user instance from me list
        # me_instance = None
        # if me != []:
        #     me_instance = me[0]

        # Getting gang information from user
        user = request.user
        user_gang_applications = Application.objects.filter(
            Q(first__gang=user.gang) | Q(second__gang=user.gang) | Q(third__gang=user.gang)
        )

        return render(request, 'accounts/profile_admin.html', {
            # 'me' : me_instance,
            'interviews' : interviews,
            'user_gang_applications': user_gang_applications,
        })
    # Normal profile
    application = Application.objects.filter(applicant=request.user).first()

    # If interview exixsts for this user, get interview instance
    if Interview.objects.filter(applicant=request.user).first():
        interview = Interview.objects.get(applicant=request.user)
    else:
        interview = None

    positions = []
    if application != None:
        positions = application.get_positions()

    return render(request, 'accounts/profile.html', {
        'positions': positions,
        'interview': interview,
    })

@login_required
def edit_profile(request):
    if request.method == 'GET':
        form = EditUserForm(instance=request.user)
    else: # POST
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse('accounts:profile') )
    # GET or form failed
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
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
            return HttpResponseRedirect( reverse('home') )

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
    allowed_statuses = ['ID', 'AC', 'PP', 'NM', 'IC']
    application = get_object_or_404(Application, applicant_id=userID)
    positions = application.get_positions()
    if len(positions) == 1:
        positions = positions * 2
    applicant = application.applicant
    date, created = Date.objects.get_or_create(user=applicant)
    userstatus = applicant.get_status()
    interview = Interview.objects.filter(applicant=application.applicant).first()

    user = request.user
    user_gang_applications = Application.objects.filter(
        Q(first__gang=user.gang) | Q(second__gang=user.gang) | Q(third__gang=user.gang)
    )

    if request.method == 'POST':
        if user.is_superuser:
            form = StatusForm(instance=applicant)
        else:
            form = RestrictedStatusForm(instance=applicant)

        chosen_time = request.POST.get('interviewtime') # Get the time marked in front-end

        if chosen_time == None:
            if user.is_superuser:
                form = StatusForm(request.POST, instance=applicant)
            else:
                form = RestrictedStatusForm(request.POST, instance=applicant)

            if form.is_valid():
                print('form valid')
                form.save()
        else:
            chosen_room = request.POST.get('interviewroom') # Get the room chosen in front-end
            chosen_interviewers = []
            delete_op = True
            for inter in request.POST.get('interviewers').split(','):
                if inter == 'None':
                    chosen_interviewers.append(None)
                else:
                    chosen_interviewers.append(User.objects.get(email=inter))
                    delete_op = False
            print('Chosen time: ' + str(chosen_time))
            print('Chosen room: ' + str(chosen_room))
            print('Chosen interviewers: ' + str(chosen_interviewers))
            print(delete_op)


            # Updating the interviewers availability
            if chosen_time != application.get_interview_time():
                # Remove old unavailable times
                if interview:
                    for inter in interview.interviewers.all():
                        userdate = Date.objects.get(user=inter)
                        userdate.add_time(application.get_interview_time())
                        userdate.save()

                # Add new unavailable times
                for inter in chosen_interviewers:
                    if inter:
                        userdate = Date.objects.get(user=inter)
                        userdate.remove_time(chosen_time)
                        userdate.save()

                application.set_interview_time(chosen_time)
                application.save()
                print('Interview time set to: ' + application.pretty_interview_time())


            # Update/create interview object
            if interview:
                interview.delete()
                interview = None
            if not delete_op: # If not delete operation
                interview = Interview.objects.create(applicant=application.applicant)
                for i in range(len(chosen_interviewers)):
                    if chosen_interviewers[i]:
                        interview.interviewers.add(chosen_interviewers[i])
                        if i == 0:
                            interview.first = chosen_interviewers[i]
                        elif i == 1:
                            interview.second = chosen_interviewers[i]
                        elif i == 2:
                            interview.third = chosen_interviewers[i]
                interview.room = chosen_room
                interview.set_interview_time(chosen_time)
                interview.save()
                print('Created interview object!')


    # GET or form failed:
    else:
        if user.is_superuser:
            form = StatusForm(instance=applicant)
        elif userstatus in allowed_statuses:
            form = RestrictedStatusForm(instance=applicant)
        else:
            form = None

    return render(request, 'accounts/manage_profile.html', {
        'application': application,
        'date': date,
        'form': form,
        'positions': positions,
        'interview': interview,
        'user_gang_applications': user_gang_applications
    })

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect( reverse('accounts:profile') )
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
    })



def widgets(request):
    form = WidgetsForm()
    return render(request, 'accounts/widgets.html', {'form': form})
