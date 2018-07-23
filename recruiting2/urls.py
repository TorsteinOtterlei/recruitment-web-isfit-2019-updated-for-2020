"""recruiting2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from job import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('position/', include('job.urls')),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', login, {'template_name':'registration/login.html'}, name='login'),
    path('profile/', views.profile, name='profile'),
    path('position_detail/<int:pk>', views.PositionDetail.as_view(), name='position_detail'),
    path('logout/', logout, {'template_name':'registration/logout.html'}, name='logout'),
    path('apply/', views.apply, name='apply'),
    path('applications/', views.applications, name='applications'),
    path('information/', views.information, name='information'),
    path('view_applications/', views.view_applications, name='view_applications'),
    path('applicant_text/<int:pk>', views.ApplicationDetail.as_view(), name='applicant_text'),
    path('all_applications/', views.all_applications, name='all_applications'),
    path('calendar/', views.calendar, name='calendar'),
    #path('rankTest', views.rankTest, name='rankTest'),
    #path('application_form/<int:position_id>/', views.PositionDetailView.as_view(), name='position_details'),
]
