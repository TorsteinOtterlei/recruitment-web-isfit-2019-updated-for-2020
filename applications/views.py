from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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
    application, created = Application.objects.get_or_create(applicant=request.user)
    applied_to = None
    if application is not None:
        form = ApplicationForm(instance=application)
        applied_to = [pos.title for pos in application.get_positions()]
        print(applied_to)
    else:
        form = ApplicationForm(request.POST, instance=application)
    if request.method == 'POST':
        selected_positions = request.POST.get('selected_positions', '').split('||')
        form = ApplicationForm(request.POST, instance=application)
        if (selected_positions[0] != ''): # if any jobs were selected
            if form.is_valid():
                application = form.save(commit=False)
                application.second = None
                application.third = None

                application.first = Position.objects.get(title = selected_positions[0])
                if len(selected_positions) > 1:
                    application.second = Position.objects.get(title = selected_positions[1])
                if len(selected_positions) > 2:
                    application.third = Position.objects.get(title = selected_positions[2])

                application.applicant = request.user
                application.save()
                return redirect('applications:set_dates')

    return render(request, 'applications/application_form.html', {
        'positions': Position.objects.all(),
        'form':form,
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'applied_to':applied_to,
    })

@login_required
def set_dates(request):
    if request.method == 'POST':
        times = request.POST.get('times')
        date = Date.objects.get(user=request.user)
        date.dates = times
        date.save()
        return redirect('../../account')
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
