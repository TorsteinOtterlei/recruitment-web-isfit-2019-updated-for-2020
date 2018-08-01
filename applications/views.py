from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
# local
from applications.forms import ApplicationForm
from applications.models import Application
# other apps
from jobs.models import Section, Gang, Position

# Create your views here.

def applications(request):
    return render(request, 'applications/applications.html', {
        'gangs': Gang.objects.all(),
    })

def view_applications(request):
    return render(request, 'applications/view_applications.html', {
        'applications': Application.objects.all(),
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'pos': Position.objects.all(),
    })


def all_applications(request):
    return render(request, 'applications/all_applications.html', {
        'applications': Application.objects.all(),
    })


class ApplicationDetail(generic.DetailView):
    model = Application
    template_name = 'applications/applicant_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = Application.text
        return context

@login_required
def apply(request):
    application = Application.objects.filter(applicant=request.user).first()
    applied_to = None
    if application is not None:
        form = ApplicationForm(instance=application)
        applied_to = application.first.title
        if application.second is not None:
            applied_to += ',' + application.second.title
            if application.third is not None:
                applied_to += ',' + application.third.title
    else:
        form = ApplicationForm(request.POST, instance=application)
    if request.method == 'POST':
        selected_positions = request.POST.get('selected_positions', '').split('||')
        print(selected_positions)
        form = ApplicationForm(request.POST, instance=application)
        if (len(request.POST.get('selected_positions', '')) != 0): # if any jobs were selected
            if form.is_valid():

                application = form.save(commit=False)

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
        # TODO: Replace user_dates
        times = request.POST.get('times')
        application = Application.objects.filter(applicant=request.user).first()
        application.dates = times
        application.save()
        return redirect('../../account')
    else:
        return render(request, 'applications/set_dates.html', {
            'user_dates': Application.objects.get(applicant=request.user).dates_list()
        })
