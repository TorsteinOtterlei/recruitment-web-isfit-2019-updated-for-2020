from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ApplicationForm
from django.views import generic
from .models import Gang, Application, Job
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class JobView(generic.ListView):
    template_name = 'job/jobs.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        self.description = get_object_or_404(Job, name=self.kwargs['description'])
        return Job.objects.filter(description=self.description)


class JobDetail(generic.ListView):
    template_name = 'job/job_details.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Application.objects.all()


def profile(request):
    jobs = None
    if Application.objects.filter(applicant=request.user).first():
        user_application = Application.objects.filter(applicant=request.user).first()
        jobs= user_application.jobs.all()

    return render(request, 'job/profile.html', {
        'jobs':jobs
    })


def index(request):
    return render(request, 'job/index.html')


def applications(request):
    return render(request, 'job/applications.html', {
        'gangs':Gang.objects.all(),


    })


@login_required
def apply(request):
    form = ApplicationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            form.save_m2m()
            return redirect('profile')
    return render(request, 'job/application_form.html', {'jobs': Job.objects.all(), 'form':form})


def application_edit(request):
    application = Application.objects.filter(applicant=request.user).first()
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            form.save_m2m()
            return(redirect('profile'))
    else:
        form = ApplicationForm(instance=application)
    return render(request, "job/application_form.html", {'jobs': Job.objects.all(), 'form':form})

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


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    render(request, 'job/logout.html')
