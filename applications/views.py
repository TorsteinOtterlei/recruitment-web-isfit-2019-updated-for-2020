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

# BUG: Unable to handle less than 3 positions
@login_required
def apply(request):
    application = Application.objects.filter(applicant=request.user).first()
    applied_to = None
    if application is not None:
        form = ApplicationForm(instance=application)
        applied_to = [pos.title for pos in application.get_positions()]
        print(applied_to)
    else:
        form = ApplicationForm(request.POST, instance=application)
    if request.method == 'POST':
        selected_positions = request.POST.get('selected_positions', '').split('||')
        form = ApplicationForm(request.POST, instance=application)
        if (selected_positions[0] != ''): # if any jobs were selected
            if form.is_valid():
                application = form.save(commit=False)
                application.second = None
                application.third = None

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
        application = Application.objects.get(applicant=request.user)
        application.dates = times
        application.save()
        return redirect('../../account')
    else:
        return render(request, 'applications/set_dates.html', {
            'user_dates': Application.objects.get(applicant=request.user).dates_list()
        })


def manage_applications(request):
    if request.method == 'POST':
        print("Posting")
        app = Application()
        #app.applicant = request.user
        return redirect('application/' + str(app.applicant.id))
    print("Getting")
    return render(request, 'applications/manage_applications.html', {
        'applicants': Application.objects.all(),
    })

def manage_profile(request, user_id):
    print("1---")
    print(user_id)
    print("2---")
    print(type(user_id))
    u = User.objects.get(id=user_id)
    print("3---")
    print(u)
    user = get_object_or_404(User, id=user_id)
    print("4---")
    print(user)
    print("5---")
    print(user_id)
    #if request.method == 'POST':
    #    redirect('#')
    return render(request, 'applications/manage_profile.html', {
        'user': user,
    })