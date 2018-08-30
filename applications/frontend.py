from django.contrib.auth.decorators import login_required, user_passes_test
#from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from jobs.models import Position
from accounts.models import User
from applications.models import Application
from random import randint

def create_dummy_user():
    try:
        r = str(randint(0,10000))
        return User.objects.create_user(
        email="dummy{}@dummy.no".format(r),
        first_name=r,
        last_name=r,
        password=r
        )
    except:
        create_dummy_user()


@login_required()
def appLength(request):
    # Is compared to applications queryset in manage_applications
    Application.objects.create(applicant=create_dummy_user(), first=Position.objects.first())
    appLength = Application.objects.exclude(first=None, second=None, third=None).count()
    return JsonResponse({'appLength': appLength})
