from django.urls import path
from applications import views

app_name = 'applications'

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('applicant_text/<int:pk>', views.ApplicationDetail.as_view(), name='applicant_text'),
    path('set_dates/', views.set_dates, name='set_dates'),
    path('manage_applications/', views.manage_applications, name='manage_applications'),
]
