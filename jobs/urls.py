from django.urls import path
from . import views
#from django.contrib.auth.views import login

app_name = 'jobs'

urlpatterns = [
    path('positions', views.PositionView.as_view(), name='positions'),
    #path('jobs/<int:jobs_id>', views.JobsDetailView.as_view(), name='jobs_details'),
    path('position_detail/<int:pk>', views.PositionDetail.as_view(), name='position_detail'),
    path('information/', views.information, name='information'),

]
