from django.urls import path
from applications import views

app_name = 'applications'

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('applications/', views.applications, name='applications'),
    path('view_applications/', views.view_applications, name='view_applications'),
    path('applicant_text/<int:pk>', views.ApplicationDetail.as_view(), name='applicant_text'),
    path('all_applications/', views.all_applications, name='all_applications'),
    path('set_dates/', views.set_dates, name='set_dates'),
]
