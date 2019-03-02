from django.urls import path
from apps.applications import views, frontend

app_name = 'applications'

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('set_dates/', views.set_dates, name='set_dates'),
    path('manage_applications/', views.manage_applications, name='manage_applications'),
    path('pling_fest/', views.pling_fest, name='pling_fest'),

    # Front-end requests:
    path('appLength/', frontend.appLength, name='appLength')
]
