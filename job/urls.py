from django.urls import path
from . import views
from django.contrib.auth.views import login

app_name = 'job'

urlpatterns = [
    path('positions', views.PositionView.as_view(), name='positions'),
    #path('jobs/<int:job_id>', views.JobDetailView.as_view(), name='job_details'),
]
