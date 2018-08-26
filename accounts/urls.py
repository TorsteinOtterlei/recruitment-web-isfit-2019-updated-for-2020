from django.urls import path
from django.contrib.auth.views import login, logout
# local:
from accounts import views
from accounts.forms import CustomAuthenticationForm
# other apps:


app_name = 'accounts' # Necessary for url naming. eg {% url 'accounts:signin' %}

urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    #path('login/', views.login_view, name='login'),
    path('login/', login, {'template_name':'accounts/login.html', 'authentication_form': CustomAuthenticationForm}, name='login'),
    path('logout/', logout, {'template_name':'jobs/home.html'}, name='logout'),
    path('<int:userID>', views.manage_profile, name='manage_profile'),
    path('widgets/', views.widgets, name='widgets'),
    path('send_mail/<int:userID>', views.send_mail, name="send_mail"),
    path('edit', views.edit_profile, name='edit_profile'),
]
