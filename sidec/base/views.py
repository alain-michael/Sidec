import datetime
from django import urls
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db.models import Avg , Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.urls import reverse
from random import shuffle
from .models import *
from .utils import avg
from .token import generate_token
from sidec.settings import *
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
            user = User.objects.filter(email=email)
            if len(user) > 0 and not user[0].is_active:
                print(user[0].is_active)
                return redirect('verify_email')
            messages.error(request, 'Log in failed. Try again.')
            return render(request, 'getstarted/login.html')
    return render(request, 'getstarted/login.html', context)

def send_email(subject, type_of_email, to_emails):
    if type_of_email == 'verify':
        template = 'new-email.html'
    html_message = render_to_string(template)
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(
        from_email=EMAIL_HOST_USER,
        to=to_emails,
        body=plain_message,
        subject=subject,
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()

def resend_verification(request, user):
    current_site = get_current_site(request)
    subject = "Sidec Confirmation Email"
    html_message = render_to_string('new-email.html', {  
    'user': user,  
    'domain': current_site.domain,  
    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
    'token':generate_token.make_token(user),  
    })
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(
        from_email=EMAIL_HOST_USER,
        to=[user.email],
        body=plain_message,
        subject=subject,
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()


def verify_email(request):
    user = request.user
    return render(request, 'verifyemail.html', {'user': user})

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and generate_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request, 'verified.html')  
    else:  
        return HttpResponse('Activation link is invalid!')  

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
                new_user = User.objects.create_user(email=email, password=ps1)
                new_user.first_name = fname
                new_user.last_name = lname
                new_user.is_active = False
                student = Student(user=new_user, level=education_level, country=country)
                student.save()
                new_user.save()
                messages.success(request, 'Account Successfully Created.')
                current_site = get_current_site(request)
                subject = "Sidec Confirmation Email"
                html_message = render_to_string('new-email.html', {  
                'user': new_user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),  
                'token':generate_token.make_token(new_user),  
                })
                plain_message = strip_tags(html_message)
                email = EmailMultiAlternatives(
                    from_email=EMAIL_HOST_USER,
                    to=[new_user.email],
                    body=plain_message,
                    subject=subject,
                )
                email.attach_alternative(html_message, 'text/html')
                email.send()
                return redirect('verify_email')
    context = {'status': 'active'}
    return render(request, 'getstarted/login.html', context)

def signout(request):
    logout(request)
    return redirect('home')
        
def dashboard(request):
    datetime_one_week_ago = timezone.now() - datetime.timedelta(days=7)

    student = request.user.student
    completed = []
    not_completed = []
    enrolled_courses = Course.objects.filter(enrolled_students__in=[student])
    upcoming_quizzes = Quiz.objects.filter(week__course__in=enrolled_courses, due_date__gte=timezone.now()).order_by('due_date')
    for course in enrolled_courses:
        student_grade = QuizGrade.objects.filter(student=student, quiz__week__course=course)
        all_quizzes = Quiz.objects.filter(week__course=course)
        if len(all_quizzes) == len(student_grade) and all((grade.marks_obtained * 100 / grade.total_marks) > 79 for grade in student_grade):
            completed.append(course)
        else:
            not_completed.append(course)
    enrolled_courses = {'completed': completed, 'not_completed': not_completed}
    completed_splits = {'completed': len(completed)*100/(len(completed)+len(not_completed)), 'not_completed': len(not_completed)*100/(len(completed)+len(not_completed))}
    week_statuses = WeekStatus.objects.filter(student=student)
    full_grades = QuizGrade.objects.filter(student=student).select_related('quiz__week__course')
    week_grades = QuizGrade.objects.filter(student=student, modified_at__gte=datetime_one_week_ago)
    user_achievements = UserAchievement.objects.filter(student=student)
    if len(week_grades) > 0:
        labels = [str(grade.modified_at.date()) for grade in full_grades]
        grades = [(grade.marks_obtained * 100 / grade.total_marks) for grade in full_grades]
        avg_week_grade = avg(grades)
    else:
        grades = []
        avg_week_grade = 0
    context = {'user': request.user, 'student':student, "average_grade": avg_week_grade, 'achievements': user_achievements, 'week_grades': week_grades, 'upcoming_quizzes': upcoming_quizzes, 'enrolled_courses': enrolled_courses, 'completed_splits': completed_splits, 'grades': grades, 'labels': labels, 'full_grades': full_grades}
    return render(request, 'main_pages/dashboard.html', context)

def questions(request):
    return render(request, 'main_pages/questions.html')

def resource_material(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    criteria1 = Q(subject=resource.subject)
    criteria2 = Q(level=resource.level)
    similar_resources = Resource.objects.filter(criteria1 & criteria2).exclude(id=resource_id)
    context = {'resource': resource, 'student': Student.objects.get(user=request.user), 'similar_resources': similar_resources}
    return render(request, 'questions/june2023.html', context)

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
        print(request.POST)
        student = Student.objects.get(user=request.user)
        socials = Socials.objects.filter(student=student)
        if len(socials) == 0:
            socials = Socials(student=student)
            socials.save()
        else:
            socials = socials[0]
        if request.FILES:
            student.profile_pic = request.FILES['profile_pic']
        if 'preferred_name' in request.POST and request.POST['preferred_name'] != '':
            student.preferred_name = request.POST['preferred_name']
        if 'user' in request.POST and request.POST['user'] != '':
            full_name: list = request.POST['user'].strip().split(' ')
            student.user.first_name = ''.join(full_name[:-1])
            student.user.last_name = full_name[-1]
        if 'email' in request.POST and request.POST['email'] != '':
            student.user.email = request.POST['email']
        if all(i in request.POST for i in ['current_password', 'new_password', 'confirm_password']):
            new_pass = request.POST['new_password']
            confirm_pass = request.POST['confirm_password']
            current_pass = request.POST['current_password']
            auth_user = authenticate(email=request.user.email, password=current_pass)
            if(confirm_pass == new_pass and auth_user is not None):
                auth_user.set_password(confirm_pass)
                messages.success(request, 'Password successfully changed.')
            elif auth_user is not None:
                messages.error(request, 'Your new password does not match the confirm password.')
            else:
                messages.error(request, 'Incorrect current password.')
        if 'bio' in request.POST and request.POST['bio'] != '':
            student.bio = request.POST['bio']
        if 'country' in request.POST and request.POST['country'] != '':
            student.country = request.POST['country']
        if 'phone' in request.POST and request.POST['phone'] != '':
            socials.number = request.POST['phone']
        if 'linkedin' in request.POST and request.POST['linkedin'] != '':
            socials.linkedin = request.POST['linkedin']
        if 'git' in request.POST and request.POST['git'] != '':
            socials.github = request.POST['git']
        if 'twitter' in request.POST and request.POST['twitter'] != '':
            socials.twitter = request.POST['twitter']
        if 'facebook' in request.POST and request.POST['facebook'] != '':
            socials.facebook = request.POST['facebook']

        print(student.__dict__)

        student.save()
        student.user.save()
        socials.save()
        return redirect('settings')
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

def save_course(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        student = Student.objects.get(id=int(body['student_id']))
        course = Course.objects.get(id=int(body['course']))
        if course in student.saved_courses.all():
            student.saved_courses.remove(course)
        else:
            student.saved_courses.add(course)
        student.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def course_page(request, id):
    course = Course.objects.get(id=id)
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        student.enrolled_courses.add(course)
        student.save()
        return redirect('course', course_id=id)
    weeks = CourseWeek.objects.filter(course=course)
    full_weeks = []
    for week in weeks:
        materials = week.materials.all()
        total_time = 0
        for material in materials:
            total_time += material.time_to_complete
        #     if material.material_type == CourseMaterial.TEXT:
        #         total_time += len(material.text.split(' ')) // 20 
        total_time = f"{min(1, int(total_time/60)) * (str(total_time//60) + 'hr')}{'s' if total_time > 119 else ''}{total_time%60} mins" 
        quizzes = week.quiz_set.all()
        full_weeks.append({'week': week, 'materials': materials, 'quizzes': quizzes, 'total_time': total_time})
    context = {'course': course, 'student': student, 'full_weeks': full_weeks}
    return render(request, 'how_to_navigate_sidec/htusidec.html', context)

def material_page(request, course_id, material_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    material = CourseMaterial.objects.get(id=material_id)
    context = {'course': course, 'material': material, 'student': student}
    return render(request, 'how_to_navigate_sidec/firstpage.html', context)

def quiz_page(request, course_id, quiz_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    quiz = Quiz.objects.get(id=quiz_id)
    grade = QuizGrade.objects.filter(student=student, quiz=quiz)
    total_marks = Question.objects.filter(quiz=quiz)
    total_marks = sum([int(i.marks) for i in total_marks])
    percentage = 0
    if len(grade) > 0:
        grade = grade.latest('modified_at')
        percentage = round(grade.marks_obtained * 100 / total_marks, 1)
        if int(percentage) == percentage:
            percentage = int(percentage)
    else:
        grade = None
    context = {'course': course, 'student': student, 'quiz': quiz, 'material': {'material_type': 'Quiz'}, 'grade': grade, 'total_marks': total_marks, 'percentage': percentage}
    return render(request, 'how_to_navigate_sidec/firstpage.html', context)

def questions_page(request, course_id, quiz_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).order_by('?')
    context = {'course': course, 'student': student, 'questions': questions}
    return render(request,'how_to_navigate_sidec/quizesone.html', context)

def mark_quiz(request, quiz_id):
    student = Student.objects.get(user=request.user)
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        questions = list(filter(lambda x: 'question' in x ,request.POST))
        total = 0
        print(request.POST)
        for question in questions:
            question_marks = 0
            total_marks = 0
            question_answers = Answer.objects.filter(question_id=question.split('_')[-1], is_correct=True)
            correct_answers = []
            for correct_answer in question_answers:
                correct_answers.append(correct_answer.id)
            for given_answer in request.POST.getlist(question):
                try:
                    if int(given_answer) in correct_answers:
                        question_marks += Question.objects.get(id=question.split('_')[-1]).marks
                    else:
                        question_marks -= Question.objects.get(id=question.split('_')[-1]).marks
                    total_marks += Question.objects.get(id=question.split('_')[-1]).marks
                except:
                    if given_answer in [answer.answer_text for answer in question_answers]:
                        question_marks += Question.objects.get(id=question.split('_')[-1]).marks
                        total_marks += Question.objects.get(id=question.split('_')[-1]).marks
                        break
                    else:
                        question_marks = 0
                    total_marks += Question.objects.get(id=question.split('_')[-1]).marks
            question_avg = question_marks / len(question_answers)
            total += max(0, question_avg)
        if QuizGrade.objects.filter(student=student, quiz=quiz).count() == 0:
            quiz_grade = QuizGrade.objects.create(quiz=quiz, student=student, marks_obtained=total, total_marks=total_marks)
            quiz_grade.save()
        else:
            quiz_grade = QuizGrade.objects.get(student=student, quiz=quiz)
            quiz_grade.marks_obtained = total
            quiz_grade.save()
    return redirect(urls.reverse('quiz_page', args=[quiz.week.course.id, quiz.id]))

def resources(request):
    resources = Resource.objects.all()
    context = {'resources': resources}
    return render(request, 'main_pages/resources.html', context)

def questions(request):
    questions = Resource.objects.filter(resource_type='QNS')
    context = {'questions': questions}
    return render(request, 'sub_pages/solutions.html', context) 

def solutions(request):
    solutions = Resource.objects.filter(resource_type='SOL')
    context = {'solutions': solutions}
    return render(request, 'sub_pages/solutions.html', context) 

def forgotpass(request):
    return render(request, 'resetpass.html')

def default(request):
    return render(request, '404.html')

def settings(request):
    student = Student.objects.get(user=request.user)
    context = {'student': student}
    return render(request, 'main_pages/settings.html', context)

def science(request):
    return render(request, 'sub_pages/science.html')

def grades(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    grades = QuizGrade.objects.filter(student=student, quiz__week__course=course)
    total = {'obtained': sum([i.marks_obtained for i in grades]), 'possible': sum([i.total_marks for i in grades])}
    context = {'student': student, 'grades': grades, 'course': course, 'total': total}
    return render(request, 'how_to_navigate_sidec/grades.html', context)

def category_page(request, category):
    courses = Course.objects.filter(category=category)
    context = {'courses': courses}
    return render(request, 'main_pages/courses.html', context)
