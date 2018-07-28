"""recruiting URL Configuration

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
from jobs import views as jobs_views
#from django.contrib.auth.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jobs_views.home, name='home'),
    path('position/', include('jobs.urls')),
    path('account/', include('accounts.urls')),
    path('application/', include('applications.urls')),
    #path('rankTest', jobs_views.rankTest, name='rankTest'),
    #path('application_form/<int:position_id>/', jobs_views.PositionDetailView.as_view(), name='position_details'),
]
