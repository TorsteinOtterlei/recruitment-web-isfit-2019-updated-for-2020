from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.views import generic
from .models import Applicant, Application, Job, Job_Detail


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

def base(request):
    return render(request, 'job/base.html')

def apply(request):#, applicant_id):
    #applicant = get_object_or_404(Applicant, id=applicant_id)
    return render(request, 'job/apply.html')#, {'applicant':applicant})

def cant_apply(request):#, applicant_id):
    #applicant = get_object_or_404(Applicant, id=applicant_id)
    return render(request, 'job/cant_apply.html')#, {'applicant':applicant})

def thanks(request):#, applicant_id):
    #applicant = get_object_or_404(Applicant, id=applicant_id)
    return render(request, 'job/thanks.html')#, {'applicant': applicant})


class UserFormView(View):
    form_class = UserForm
    template_name = 'job/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('job:index')

        return render(request, self.template_name, {'form': form})