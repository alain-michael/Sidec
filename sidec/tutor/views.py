from django.shortcuts import render
from base.models import *

# Create your views here.

def tutor_index(request):
    return render(request, 'sidec_admin-main/index.html')

def tutor_dashboard(request):
    context = {'tutor': Tutor.objects.get(user=request.user)}
    return render(request, 'sidec_admin-main/home/dashboard.html', context)

def tutor_new_course(request):
    context = {'tutor': Tutor.objects.get(user=request.user)}
    return render(request, 'sidec_admin-main/home/new-course.html', context)

def tutor_add_course(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'sidec_admin-main/home/new-course.html', context)