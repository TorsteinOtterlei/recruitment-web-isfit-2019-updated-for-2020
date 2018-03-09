from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ApplicationForm
from django.views import generic
from .models import Gang, Application, Position, Section
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PositionView(generic.ListView):
    template_name = 'job/positions.html'
    context_object_name = 'all_positions'

    def get_queryset(self):
        self.description = get_object_or_404(Position, name=self.kwargs['description'])
        return Position.objects.filter(description=self.description)


class PositionDetail(generic.ListView):
    template_name = 'job/position_details.html'
    context_object_name = 'all_positions'

    def get_queryset(self):
        return Application.objects.all()

@login_required
def profile(request):
    positions = None
    if Application.objects.filter(applicant=request.user).first():
        user_application = Application.objects.filter(applicant=request.user).first()
        positions= user_application.positions.all()

    return render(request, 'job/profile.html', {
        'positions':positions
    })


def index(request):
    return render(request, 'job/index.html')


def applications(request):
    return render(request, 'job/applications.html', {
        'gangs':Gang.objects.all(),


    })

def view_applications(request):
    return render(request, 'job/view_applications.html', {
        'applications': Application.objects.all(),
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'pos': Position.objects.all(),
    })


@login_required
def apply(request):
    application = Application.objects.filter(applicant=request.user).first()
    applied_to = None
    if application is not None:
        form = ApplicationForm(instance=application)
        applied_to = application.positions.all()
    else:
        form = ApplicationForm(request.POST, instance=application)
    if request.method == 'POST':
        positions = request.POST.getlist('positions', None)
        form = ApplicationForm(request.POST, instance=application)
        if positions: # if any jobs were selected
            if application is not None: # if user already has an application
                if form.is_valid():
                    application = form.save(commit=False)
                    application.applicant = request.user
                    application.positions.clear()
                    application.save()
                    for position in positions:
                        application.positions.add(position)
                    application.save()
                    return (redirect('profile'))
            else:  # create new application
                if form.is_valid():
                    application = form.save(commit=False)
                    application.applicant = request.user
                    application.save()
                    for position in positions:
                        application.positions.add(position)
                    application.save()
                    return redirect('profile')
        else:
            pass  # can't make am application to no positions :S

    return render(request, 'job/application_form.html', {
        'positions': Position.objects.all(),
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

def information(request):
    return render(request, 'job/information.html', {
        'sections': Section.objects.all(),
        'gangs': Gang.objects.all(),
        'positions':Position.objects.all()
    })
