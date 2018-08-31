from django.contrib.auth.decorators import login_required, user_passes_test
#from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from jobs.models import Position
from accounts.models import User
from applications.models import Application
from random import randint

def create_dummy_user():
    try:
        r = str(randint(0,100000))
        return User.objects.create_user(
        email="pling{}@dummy.no".format(r),
        first_name="Pling",
        last_name=r,
        password=r
        )
    except:
        create_dummy_user()


@login_required()
def appLength(request):
    # NOTE: Application creation is only for testing
    #Application.objects.create(applicant=create_dummy_user(), first=Position.objects.first())
    appLength = Application.objects.exclude(first=None, second=None, third=None).count()
    return JsonResponse({'appLength': appLength})
