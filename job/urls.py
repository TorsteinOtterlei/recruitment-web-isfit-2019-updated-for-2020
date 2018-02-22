from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.UserFormView.as_view(), name='register'),
    path('apply', views.apply, name='apply'),
    path('cant_apply', views.cant_apply, name='cant_apply'),
    path('apply/thanks', views.thanks, name='thanks'),
    path('base', views.base, name='base'),
    path('jobs', views.JobView.as_view(), name='jobs'),
    path('jobs/<int:job_id>', views.JobDetailView.as_view(), name='job_details')
]