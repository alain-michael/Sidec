from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from .models import *
from .utils import avg
import json
# Create your views here.

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        courses = Course.objects.select_related('course_tutor').filter(price=0)
        print(courses)
        context = {"student": student, 'courses': courses}
        return render(request, 'main_pages/discover.html', context)
    else:
        return render(request, 'getstarted.html')

def signin(request):
    context = {'status': ''}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            messages.success(request, 'Logged in successfully')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Log in failed. Try again.')
            return render(request, 'getstarted/login.html')
    return render(request, 'getstarted/login.html', context)

def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        names = name.split(' ')
        fname = ' '.join(names[:-1])
        lname = names[-1]
        email = request.POST["email"]
        education_level = request.POST["education-level"]
        country = request.POST["country"]
        ps1 = request.POST["ps1"]
        ps2 = request.POST["ps2"]

        if ps1 == ps2:
            try:
                new_user = User.objects.create_user(email=email, password=ps1)
                new_user.first_name = fname
                new_user.last_name = lname
                print(new_user)
                student = Student(user=new_user, level=education_level, country=country)
                student.save()
                new_user.save()
                print(student)
                messages.success(request, 'Account Successfully Created.')
                if request.user.is_authenticated:
                    logout(request)
                return redirect('home')
            except:
                messages.error(request, 'There was a problem with account creation. Try again.')
    context = {'status': 'active'}
    return render(request, 'getstarted/login.html', context)

def signout(request):
    logout(request)
    return redirect('home')
        
def dashboard(request):
    student = request.user.student
    week_statuses = WeekStatus.objects.filter(student=student)
    week_grades = Grade.objects.select_related('week_status__week__course').filter(week_status__in=week_statuses)
    user_achievements = UserAchievement.objects.filter(student=student)
    
    if len(week_grades) > 0:
        avg_week_grade = avg(week_grades, 'grade')
    else:
        avg_week_grade = 0
    
    context = {'user': request.user, 'student':student, "average_grade": avg_week_grade, 'achievements': user_achievements, 'week_grades': week_grades}
    return render(request, 'main_pages/dashboard.html', context)

def courses(request):
    courses = Course.objects.all()
    paid_courses = []
    free_courses = []
    for course in courses:
        if course.price > 0:
            paid_courses.append(course)
        else:
            free_courses.append(course)
    context = {'student': Student.objects.get(user=request.user), 'paid_courses': paid_courses, 'free_courses': free_courses}
    return render(request, 'main_pages/courses.html', context)

def course(request, course_id):
    course = Course.objects.select_related('course_tutor').get(id=course_id)
    student = Student.objects.get(user=request.user)
    comments = CourseComment.objects.filter(course=course)
    if request.method == 'POST' and 'add_comment' in request.POST:
        comment_text = request.POST['comment-box']
        new_comment = CourseComment(course=course, student=student, comment=comment_text)
        new_comment.save()
    context = {'course': course, 'student': student, 'comments': comments[::-1]}
    return render(request, 'enrol_pages/enrol2.html', context)

def delete_comment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        comment = CourseComment.objects.get(id=body['comment_id'])
        comment.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def edit_comment(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        comment_edit = body['comment_edit']
        comment_id = body['comment_id']
        prev_comment = CourseComment.objects.get(id=comment_id)
        prev_comment.comment = comment_edit
        prev_comment.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def update_student_info(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        if request.FILES:
            student.profile_pic = request.FILES['profile_pic']
        if 'preferred_name' in request.POST:
            student.preferred_name = request.POST['preferred_name']
        if 'user' in request.POST:
            full_name: list = request.POST['user'].strip().split(' ')
            student.user.first_name = ''.join(full_name[:-1])
            student.user.last_name = full_name[-1]
        if 'email' in request.POST:
            student.user.email = request.POST['email']
        if all(request.POST[i] for i in ['current_password', 'new_password', 'confirm_password']):
            new_pass = request.POST['new_password']
            confirm_pass = request.POST['confirm_password']
            current_pass = request.POST['current_password']
            if(confirm_pass == new_pass):
                print('same')

        student.save()
        student.user.save()
        return redirect('settings')
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

def course_page(request, id):
    course = Course.objects.get(id=id)
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        student.enrolled_courses.add(course)
        return redirect('course', course_id=id)
    return HttpResponse('Course Page')

def enrol(request):
    return HttpResponse('hip')

def forgotpass(request):
    return render(request, 'resetpass.html')

def default(request):
    return HttpResponse('hip')

def settings(request):
    student = Student.objects.get(user=request.user)
    context = {'student': student}
    return render(request, 'main_pages/settings.html', context)