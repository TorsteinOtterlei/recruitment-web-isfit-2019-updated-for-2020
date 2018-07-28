from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import *
from .models import *

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
