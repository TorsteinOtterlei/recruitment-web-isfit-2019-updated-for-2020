from django.urls import path
from accounts import views
from django.contrib.auth.views import login, logout

app_name = 'accounts'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', login, {'template_name':'accounts/login.html'}, name='login'),
    path('logout/', logout, {'template_name':'jobs/home.html'}, name='logout'),
    path('<int:application_id>', views.manage_profile, name='manage_profile'),

]
