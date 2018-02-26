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

'''class JobDetailView(generic.DetailView):
    model = Job
    template_name = 'job/job_details.html'
    context_object_name = 'description'
    queryset = Job.objects.all()

    def get_context_data(self, **kwargs):
        context = JobView.get_context_data(**kwargs)
        context['description'] = self.description
        return context

def job_detail(request):
    return render(request, 'job/job_details.html')
'''

class Job_Detail(generic.ListView):
    template_name = 'job/job_details.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Application.objects.all()

class Profile(generic.ListView):
    template_name = 'job/profile.html'
    context_object_name = 'all_applications'

    def get_queryset(self):
        return Application.objects.all()


def index(request):
    return render(request, 'job/index.html')

class Apply(generic.ListView):
    template_name = 'job/apply.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Job.objects.all()


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

@login_required
def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.phone_number = form.phone_number
            application.save()
            return redirect('index')

