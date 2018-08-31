from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test

# Send mail --------------------------------------------------------------------
@login_required
@staff_member_required
def send_mail(request, userID):
    emil, created = User.objects.get_or_create(email="twidex97@gmail.com")
    user = get_object_or_404(User, id=userID)

    msg = """You have got an interview with ISFiT
            Your interview is {}
            Interviewer: {}

            Sent from {}""".format(user.application.pretty_date(), user.application.first, request.user)

    emil.email_user(subject="Interview", message=msg, from_email="emil.telstad@live.no")
    #user.email_user(subject="Interview", message=msg, from_email=request.user.email)
    return HttpResponse()
    #return manage_profile(request, userID)
# End: Send mail ---------------------------------------------------------------

# Delete user ------------------------------------------------------------------
@login_required
def delete_user(request):
    request.user.delete()
    logout(request)
    return redirect('home')
# End: Delete user -------------------------------------------------------------
