from django.urls import path
from . import views

urlpatterns = [
    path('tutor/index', views.tutor_index, name='tutor_index'),
    path('tutor/dashboard', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/new_course', views.tutor_new_course, name='tutor_new_course'),
    path('tutor/add_course', views.tutor_add_course, name='tutor_add_course'),
]
