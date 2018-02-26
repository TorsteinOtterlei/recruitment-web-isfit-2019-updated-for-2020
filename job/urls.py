from django.urls import path
from . import views
from django.contrib.auth.views import login

app_name = 'job'

urlpatterns = [
    path('jobs', views.JobView.as_view(), name='jobs'),
    #path('jobs/<int:job_id>', views.JobDetailView.as_view(), name='job_details'),
]