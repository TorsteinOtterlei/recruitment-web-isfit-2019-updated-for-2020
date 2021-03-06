from django.urls import path
# local
from apps.jobs import views

app_name = 'jobs'

urlpatterns = [
    #path('positions', views.PositionView.as_view(), name='positions'),
    #path('jobs/<int:jobs_id>', views.JobsDetailView.as_view(), name='jobs_details'),
    path('<int:pk>', views.PositionDetail.as_view(), name='position_detail'),
    path('information/', views.information, name='information'),
    path('calendar/', views.calendar, name='calendar'),
]
