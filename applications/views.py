from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.http import JsonResponse
# local
from applications.forms import ApplicationForm
from applications.models import Application
# other apps
from jobs.models import Section, Gang, Position, Date, Interview
from accounts.models import User

@login_required
def apply(request):
    # vars
    application, created = Application.objects.get_or_create(applicant=request.user)
    applied_to = None
    if application.has_positions():
        applied_to = [pos.title for pos in application.get_positions()]

    if Interview.objects.filter(applicant=request.user).first():
        interview = Interview.objects.get(applicant=request.user)
    else:
        interview = None

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid(): # if any jobs were selected
            selected_positions = request.POST.get('selected_positions', '').split('||')
            application = form.save(commit=False)
            application.set_positions(selected_positions)
            application.save()
            return redirect('applications:set_dates')

    # GET or form failed
    print(json.dumps(applied_to))
    return render(request, 'applications/application_form.html', {
        'form': ApplicationForm(instance=application),
        'positions': Position.objects.all(),
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'applied_to': json.dumps(applied_to),
        'interview': interview,
    })
    # End: apply

@login_required
def set_dates(request):
    # Temporal: deadline for interviewers was on 29. Aug -----------------------
    # if request.user.is_staff:
    #     return render(request, 'applications/set_dates.html')
    # --------------------------------------------------------------------------
    if request.method == 'POST':
        times = request.POST.get('times')
        date = Date.objects.get(user=request.user)
        date.dates = times
        date.save()
        return redirect('../../account/')
    else:
        date, created = Date.objects.get_or_create(user=request.user)
        return render(request, 'applications/set_dates.html', {
            'user_dates': date.dates_list()
        })

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_applications(request):
    # Getting user defiend setup
    display = 'email' # TODO fix so active display/sorting is saved
    sorting = 'apply_time'
    if request.method == 'POST':
        display = request.POST.get('display', False)
        sorting = request.POST.get('sorting', False)

    # Showing data depending on user type
    if request.user.is_superuser:
        applications = Application.objects
    else:
        applications = Application.objects.filter(first__gang=request.user.gang) \
            | Application.objects.filter(second__gang=request.user.gang) \
            | Application.objects.filter(third__gang=request.user.gang)
    print(applications)

    # Removing applications unfinished applications
    applications = applications.exclude(first=None, second=None, third=None)

    # Sorting based on user input
    if sorting == 'interview_time':
        unsorted_applications = applications.all()
        applications = sorted(unsorted_applications, key = lambda appl : appl.get_order_time())


    return render(request, 'applications/manage_applications.html', {
        'applications': applications,
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'status_choices': request.user.STATUS_CHOISES,
        'display': display,
        'sorting': sorting
    })
    # End manage_applications

@login_required
def pling_fest(request):
    appLength = Application.objects.exclude(first=None, second=None, third=None).count()
    return render(request, 'applications/pling_fest.html', {'appLength': appLength})
