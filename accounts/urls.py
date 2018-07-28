from django.urls import path
from . import views
from django.contrib.auth.views import login, logout

app_name = 'accounts'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', login, {'template_name':'accounts/login.html'}, name='login'),
    path('logout/', logout, {'template_name':'accounts/logout.html'}, name='logout'),

]
