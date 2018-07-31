from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
from jobs.models import Section, Gang
from applications.models import Dates

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
        applied_to = application.ranking
    else:
        form = ApplicationForm(request.POST, instance=application)
    if request.method == 'POST':

        form = ApplicationForm(request.POST, instance=application)
        if (len(request.POST.get('first', '')) != 0): # if any jobs were selected
            if form.is_valid():

                r = Ranking() # making a new ranking object
                r.first = Position.objects.get(title = request.POST.get('first', ''))

                # TODO maybe fix this hard code
                second = request.POST.get('second', '')
                third = request.POST.get('third', '')
                if (len(third) > 0):
                    r.second = Position.objects.get(title = second)
                    r.third = Position.objects.get(title = third)
                elif (len(second) > 0):
                    r.second = Position.objects.get(title = second)
                r.save()

                if application is not None: # delete old ranking
                    Ranking.objects.filter(id = application.ranking.id).delete()

                application = form.save(commit=False)
                application.ranking = r
                application.applicant = request.user
                application.save()
                return redirect('profile')

    return render(request, 'applications/application_form.html', {
        'positions': Position.objects.all(),
        'form':form,
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'applied_to':applied_to,
    })

@login_required
def set_dates(request):
    print(request)
    print(request.method)
    print("Felldfo")
    if request.method == 'POST':
        print("Fellofkr")
        # TODO: Replace user_dates
        if request.POST['times']:
            time = Dates()
            time.dates = request.POST['times']
            time.applicant = request.user
            print("Fello")
            time.save()
            print("fdker")
    else:
        return render(request, 'applications/set_dates.html', {
            'user_dates': Dates.objects.get(applicant=request.user).dates_list()
        })
