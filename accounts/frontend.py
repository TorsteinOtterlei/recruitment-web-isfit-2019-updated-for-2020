from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test


# Delete user ------------------------------------------------------------------
@login_required
def delete_user(request):
    request.user.delete()
    logout(request)
    return redirect('home')
# End: Delete user -------------------------------------------------------------
