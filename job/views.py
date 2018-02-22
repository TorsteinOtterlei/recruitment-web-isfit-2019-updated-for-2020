from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.views import generic
from .models import Gang, Application, Job


class JobView(generic.ListView):
    template_name = 'job/jobs.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Job.objects.all()

class JobDetailView(generic.DetailView):
    model = Job
    template_name = 'job/job_details.html'


def index(request):
    return render(request, 'job/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            form = SignUpForm()
        return render(request, 'job/registration_form.html', {'form':form})