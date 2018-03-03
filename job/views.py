from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ApplicationForm
from django.views import generic
from .models import Gang, Application, Job, Section
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
    application = Application.objects.filter(applicant=request.user).first()
    applied_to = None
    if application is not None:
        form = ApplicationForm(instance=application)
        applied_to = application.jobs.all()
    else:
        form = ApplicationForm(request.POST, instance=application)
    if request.method == 'POST':
        jobs = request.POST.getlist('jobs', None)
        print(jobs)
        print(not jobs)
        form = ApplicationForm(request.POST, instance=application)
        if jobs: # if any jobs were selected
            if application is not None: # if user already has an application
                if form.is_valid():
                    application = form.save(commit=False)
                    application.applicant = request.user
                    application.jobs.clear()
                    application.save()
                    for job in jobs:
                        application.jobs.add(job)
                    application.save()
                    return (redirect('profile'))
            else:  # create new application
                if form.is_valid():
                    application = form.save(commit=False)
                    application.applicant = request.user
                    application.save()
                    for job in jobs:
                        application.jobs.add(job)
                    application.save()
                    return redirect('profile')
        else:
            pass  # can't make am application to no jobs :S

    return render(request, 'job/application_form.html', {
        'jobs': Job.objects.all(),
        'form':form,
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'applied_to':applied_to

    })


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
        return render(request, 'registration/registration_form.html', {'form':form})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    render(request, 'registration/logout.html')
