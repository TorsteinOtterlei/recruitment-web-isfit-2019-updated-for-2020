from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
from applications.models import Application

def home(request):
    return render(request, 'jobs/home.html')

def information(request):
    return render(request, 'jobs/information.html', {
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'positions':Position.objects.all()
    })

class PositionView(generic.ListView):
    template_name = 'jobs/positions.html'
    context_object_name = 'all_positions'

    def get_queryset(self):
        self.description = get_object_or_404(Position, name=self.kwargs['description'])
        return Position.objects.filter(description=self.description)


class PositionDetail(generic.DetailView):
    model = Position
    template_name = 'jobs/position_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = Position.description
        return context

# IDEA: Move to jobs
# BUG: Not finished at all
@login_required
def calendar(request):
    return render(request, 'jobs/calendar.html', {
        'calendar': Calendar.objects.filter(gangleader=request.user).first(),
        'applications': list(Application.objects.all()),
        'interviews': {'pers45': 0, 'pers92': 6, 'pers118': 7, 'pers195': 11, 'pers142': 16, 'pers35': 26, 'pers70': 27, 'pers19': 28, 'pers82': 32, 'pers61': 39, 'pers128': 40, 'pers89': 41, 'pers149': 43, 'pers33': 50, 'pers123': 51, 'pers48': 52, 'pers96': 55, 'pers199': 58, 'pers178': 60, 'pers43': 61, 'pers159': 64, 'pers140': 65, 'pers34': 66, 'pers32': 68}
    })
