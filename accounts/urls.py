from django.urls import path
from django.contrib.auth.views import login, logout
# local:
from accounts import views, frontend
# other apps:


app_name = 'accounts' # Necessary for url naming. eg {% url 'accounts:signin' %}

urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    #path('login/', views.login_view, name='login'),
    path('login/', login, {'template_name':'accounts/login.html'}, name='login'),
    path('logout/', logout, {'template_name':'jobs/home.html'}, name='logout'),
    path('<int:userID>', views.manage_profile, name='manage_profile'),
    path('widgets/', views.widgets, name='widgets'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('email/<int:userID>', views.email, name='email'),
    path('export_users/xls', views.export_users_xls, name='export_users_xls'),

    # Front-end requests:
    path('delete_user/', frontend.delete_user, name="delete_user"),
]
