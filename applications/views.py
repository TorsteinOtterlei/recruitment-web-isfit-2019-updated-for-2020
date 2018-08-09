from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import json
# local
from applications.forms import ApplicationForm
from applications.models import Application
# other apps
from jobs.models import Section, Gang, Position, Date
from accounts.models import User

# Create your views here.
"""
class ApplicationDetail(generic.DetailView):
    model = Application
    template_name = 'applications/applicant_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = Application.text
        return context
"""

@login_required
def apply(request):
    # vars
    application, created = Application.objects.get_or_create(applicant=request.user)
    applied_to = None
    if application.has_positions():
        applied_to = [pos.title for pos in application.get_positions()]

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
    })
    # End: apply

@login_required
def set_dates(request):
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
@staff_member_required
def manage_applications(request):
    return render(request, 'applications/manage_applications.html', {
        'applications': Application.objects.all(),
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all()
    })
