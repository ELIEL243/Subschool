from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm
from .decorators import allowed_users
from .models import *
from .utils import CheckHomeWork
import threading
import os
import mimetypes

# Create your views here.

""" 

    AUTHENTIFICATION

"""


def Logout(request):
    logout(request)
    return redirect('login')


def Login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if request.user.groups.filter(name="student"):
                    messages.success(request, f"Bienvenue {request.user} !")
                    return redirect('home-student')
                elif request.user.groups.filter(name="teacher"):
                    messages.success(request, f"Bienvenue {request.user} !")
                    return redirect('home-teacher')
            else:
                messages.success(request, "Nom d'utilisateur ou mot de passe incorrect !")
    return render(request, 'school/login.html', context={'form': form})


""" 

    TEACHER

"""


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacher_admin(request):
    nbr_courses = Course.objects.filter(teacher=request.user.teacher).count()
    courses = Course.objects.filter(teacher=request.user.teacher)
    nbr_students = 0
    nbr_prom = 0
    test = ''
    stds = students_teacher(request)
    students = stds
    nbr_students = len(students)
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    nbr_questions = questions.filter(satisfied=False).count()

    for course in courses:
        for promo in course.promotion.all():
            if promo.name != test:
                nbr_prom += 1
            test = promo.name
    context = {'nbr_courses': nbr_courses, 'nbr_prom': nbr_prom, 'nbr_student': nbr_students, 'activehome': 'active', 'students': students, 'nbr_questions': nbr_questions}
    return render(request, 'school/home_teacher.html', context)


def students_teacher(request):
    teacher = request.user.teacher
    promotions = Promotion.objects.filter(courses__teacher=teacher)
    students = Student.objects.all()
    stds = list()
    for promotion in promotions:
        for student in students:
            if student.promotion == promotion:
                stds += [student]

    return set(stds)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def courses_teach(request):
    courses = Course.objects.filter(teacher__name=request.user.teacher.name)
    course = None
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    nbr_questions = questions.filter(satisfied=False).count()

    context = {'courses': courses, 'course1': course, 'activecourse': "active", 'nbr_questions': nbr_questions}
    return render(request, 'school/courses_teacher.html', context)


x = threading.Thread(target=CheckHomeWork)
x.start()


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def homeworks(request):
    courses = Course.objects.filter(teacher=request.user.teacher)
    duttys = HomeWork.objects.filter(course__teacher=request.user.teacher).order_by('-date')
    active_homework = "active"
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    nbr_questions = questions.filter(satisfied=False).count()

    if request.method == "POST":
        if request.POST.get('new_tp'):
            cours = Course.objects.get(name=request.POST.get('cours'))
            types = request.POST.get('type')
            file = request.FILES.get('file')
            end = request.POST.get('end')
            desc = request.POST.get('desc')
            cote = request.POST.get('cote')
            titre =request.POST.get('titre')
            if file is not None:
                HomeWork.objects.create(course=cours, title=titre,file=file, end=end, notice=desc, cote=cote, type=types)
                messages.success(request, f"{types} publié(e) avec succes !")
                return redirect('homework')
            else:
                HomeWork.objects.create(course=cours, title=titre, end=end, notice=desc, cote=cote, type=types)
                messages.success(request, f"{types} publié(e) avec succes !")
                return redirect('homework')
    context = {'duttys': duttys, 'activedut': active_homework, 'courses': courses, 'nbr_questions': nbr_questions}
    return render(request, 'school/homework.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def homeworks_det(request, pk):
    course = Course.objects.get(id=pk)
    courses = Course.objects.filter(teacher=request.user.teacher)
    duttys = HomeWork.objects.filter(course=course).order_by('-date')
    active_homework = "active"
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    nbr_questions = questions.filter(satisfied=False).count()

    if request.method == "POST":
        if request.POST.get('new_tp'):
            cours = Course.objects.get(name=request.POST.get('cours'))
            types = request.POST.get('type')
            file = request.FILES.get('file')
            end = request.POST.get('end')
            desc = request.POST.get('desc')
            cote = request.POST.get('cote')
            titre =request.POST.get('titre')
            if file is not None:
                HomeWork.objects.create(course=cours, title=titre,file=file, end=end, notice=desc, cote=cote, type=types)
                messages.success(request, f"{types} publié(e) avec succes !")
                return redirect('homework')
            else:
                HomeWork.objects.create(course=cours, title=titre, end=end, notice=desc, cote=cote, type=types)
                messages.success(request, f"{types} publié(e) avec succes !")
                return redirect('homework')
    context = {'duttys': duttys, 'course1': course, 'activedut': active_homework, 'courses': courses, 'nbr_questions': nbr_questions}
    return render(request, 'school/homeworks_det.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacher_video(request):
    videos = Video.objects.filter(course__teacher=request.user.teacher)
    courses = Course.objects.filter(teacher=request.user.teacher)
    if request.method == "POST":
        course = Course.objects.get(name=request.POST.get('course'))
        title = request.POST.get('title')
        video = request.FILES.get('video')
        Video.objects.create(course=course, title=title, video=video)
        messages.success(request, "video ajoutée avec succes !")
    return render(request, 'school/video_teacher.html', context={'courses': courses, 'videos': videos, 'activevideo': 'active'})


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def homeworkdetail(request, id):
    homework = HomeWork.objects.get(pk=id)
    active_homework = "active"
    submission = Submission.objects.filter(homework=homework)
    sub = None
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    nbr_questions = questions.filter(satisfied=False).count()

    if request.GET.get('sub_id'):
        sub_id = request.GET.get('sub_id')
        sub = Submission.objects.get(id=sub_id)
    if request.method == "POST":
        if request.POST.get('cloturer'):
            homework.completed = True
            homework.save()
            messages.success(request, f"{homework.type} cloturé avec succes !")
            return redirect('homework-detail', homework.id)

        if request.POST.get('prolong'):
            end_date = request.POST.get('end')
            homework.end = end_date
            homework.completed = False
            homework.save()
            messages.success(request, "Travail prolongé avec succes !")
            return redirect('homework-detail', id=homework.id)

        if request.POST.get('cote'):
            cote = request.POST.get('cote')
            sub.cote = cote
            sub.coted = True
            sub.save()
            messages.success(request, f"{homework.type} de {sub.student.name} coté avec succes !")
            return redirect('homework-detail', homework.id)
    context = {'homework': homework, 'submission': submission, 'activedut': active_homework, 'sub': sub, 'nbr_questions': nbr_questions}
    return render(request, 'school/homework_detail.html', context)


def course_detail(request, id):
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    nbr_questions = questions.filter(satisfied=False).count()

    course = Course.objects.get(id=id)
    if request.method == "POST":
        note = request.FILES.get('note')
        if note:
            note_create = Note.objects.create(file=note)
            course = Course.objects.get(id=id)
            course.note.add(note_create)
            messages.success(request, "document ajouté avec succes !")
            return render(request, 'school/partials.html', context={'doc': note_create})
    return render(request, 'school/partials.html', context={'course1': course, 'nbr_questions': nbr_questions})


def QR(request):
    questions = Question.objects.filter(course__teacher=request.user.teacher)
    activeqr = "active"
    nbr_questions = questions.filter(satisfied=False).count()
    context = {'activeqr': activeqr, 'questions': questions, 'nbr_questions': nbr_questions}
    return render(request, 'school/questions_teacher.html', context)


def detail_question(request, pk):
    question = Question.objects.get(id=pk)
    responses = Response.objects.filter(question=question)
    context = {'question': question, 'responses': responses}
    return render(request, 'school/detail_question.html', context)


def add_question(request):
    response = request.POST.get('response')
    owner = request.user
    question = request.POST.get('question')
    if request.user.groups.filter(name="student"):
        owner_type = "2"
    else:
        owner_type = "1"
    response1 = Response.objects.create(owner=owner, question_id=question, owner_type=owner_type, response=response)
    question1 = Question.objects.get(id=question)
    question1.satisfied = True
    question1.save()
    messages.success(request, "Repondue avec succes !")
    context = {'add_response': True, 'response': response1}
    return render(request, 'school/partials.html', context)

""" 

    STUDENT

"""


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def student_admin(request):
    courses = Course.objects.filter(Q(promotion=request.user.student.promotion) | Q(promotion=request.user.student.com_prom))
    courses = set(courses)
    nbr_msg = Response.objects.filter(question__student=request.user.student, is_read=False).count()
    return render(request, 'school/home_student.html', context={'courses': courses, 'activehome': 'active', 'nbr_msg': nbr_msg})


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def course_detail_student(request, id):
    course = Course.objects.get(id=id)
    homeworks = HomeWork.objects.filter(course=course, completed=False)
    nbr_active_homework = homeworks.count()
    return render(request, 'school/partials.html', context={'course2': course, 'homeworks': homeworks, 'nbr_homeworks': nbr_active_homework})


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def homeworks_for_student(request):
    duttys = HomeWork.objects.filter(Q(course__promotion=request.user.student.promotion) | Q(course__promotion=request.user.student.com_prom)).order_by('-date')
    nbr_msg = Response.objects.filter(question__student=request.user.student, is_read=False).count()
    submission = None
    homework = None
    courses = Course.objects.filter(
        Q(promotion=request.user.student.promotion) | Q(promotion=request.user.student.com_prom))
    courses = set(courses)
    if request.method == "POST":
        if request.POST.get('del'):
            id_sub = request.POST.get('id_sub')
            submission = Submission.objects.get(id=id_sub)
            submission.delete()
            messages.success(request, "Travail supprimé avec succes !")
            return redirect('homework-for-student')
        submission = request.FILES.get('submission')
        homework = request.POST.get('id_homework')
        dutty = HomeWork.objects.get(id=homework)
        comment = request.POST.get('comment')
        Submission.objects.create(homework_id=homework, student=request.user.student, file=submission, comment=comment)
        messages.success(request, f'{dutty.type} deposé avec succes !')
    return render(request, 'school/homeworks_student_side.html', context={'homeworks': duttys, 'activedut': 'active', 'nbr_msg': nbr_msg, 'courses': courses})


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def homeworks_for_student_det(request, pk):
    course = Course.objects.get(id=pk)
    duttys = HomeWork.objects.filter(course=course).order_by('-date')
    nbr_msg = Response.objects.filter(question__student=request.user.student, is_read=False).count()
    submission = None
    homework = None
    courses = Course.objects.filter(
        Q(promotion=request.user.student.promotion) | Q(promotion=request.user.student.com_prom))
    courses = set(courses)
    if request.method == "POST":
        if request.POST.get('del'):
            id_sub = request.POST.get('id_sub')
            submission = Submission.objects.get(id=id_sub)
            submission.delete()
            messages.success(request, "Travail supprimé avec succes !")
            return redirect('homework-for-student')
        submission = request.FILES.get('submission')
        homework = request.POST.get('id_homework')
        dutty = HomeWork.objects.get(id=homework)
        comment = request.POST.get('comment')
        Submission.objects.create(homework_id=homework, student=request.user.student, file=submission, comment=comment)
        messages.success(request, f'{dutty.type} deposé avec succes !')
    return render(request, 'school/homework_student_side_det.html', context={'homeworks': duttys, 'activedut': 'active', 'nbr_msg': nbr_msg, 'courses': courses, 'course1': course})


def homeworks_for_course(request, pk):
    course = Course.objects.get(id=pk)
    duttys = HomeWork.objects.filter(course=course).order_by('-date')
    nbr_msg = Response.objects.filter(question__student=request.user.student, is_read=False).count()

    if request.method == "POST":
        submission = request.FILES.get('submission')
        homework = request.POST.get('id_homework')
        dutty = HomeWork.objects.get(id=homework)
        comment = request.POST.get('comment')
        Submission.objects.create(homework_id=homework, student=request.user.student, file=submission, comment=comment)
        messages.success(request, f'{dutty.type} deposé avec succes !')
    return render(request, 'school/homework_for_student.html', context={'course': course, 'duttys': duttys, 'nbr_msg': nbr_msg})


def homework_detail_student(request, pk):
    homework = HomeWork.objects.get(id=pk)
    submissions = Submission.objects.filter(homework=homework)
    submission = None
    user = request.user.student
    is_sub = False
    for sub in submissions:
        if sub.student == user:
            is_sub = True
            submission = sub
    return render(request, 'school/partials.html', context={'homework': homework, 'submission': submission, 'is_sub': is_sub})


def questions_student_side(request):
    questions = Question.objects.filter(student=request.user.student)
    courses = Course.objects.filter(
        Q(promotion=request.user.student.promotion) | Q(promotion=request.user.student.com_prom))
    courses = set(courses)
    if request.method == "POST":
        course = Course.objects.get(name=request.POST.get('course'))
        title = request.POST.get('title')
        question = request.POST.get('question')
        Question.objects.create(student=request.user.student, course=course, title=title, question=question)
        messages.success(request, 'Question posée avec succes !')
        return redirect('question-student')
    return render(request, 'school/questions_student_side.html', context={'questions': questions, 'courses': courses})


def response_student_side(request, pk):
    question = Question.objects.get(id=pk)
    responses = Response.objects.filter(question=question)
    owner = request.user
    if request.method == "POST":
        question = request.POST.get('question')
        response = request.POST.get('response')
        if request.user.groups.filter(name="student"):
            owner_type = "2"
        else:
            owner_type = "1"
        response1 = Response.objects.create(owner=owner, question_id=question, owner_type=owner_type, response=response)
        question1 = Question.objects.get(id=question)
        question1.satisfied = True
        question1.save()

        messages.success(request, "Repondue avec succes !")
    context = {'responses': responses, 'question': question}
    return render(request, 'school/detail_question_student.html', context)


def get_responses_question(request, pk):
    question = Question.objects.get(id=pk)
    responses = Response.objects.filter(question=question)
    for response in responses:
        if response.owner != request.user:
            if not response.is_read:
                response.is_read = True
                response.save()
    question.satisfied = True
    question.save()
    context = {'responses': responses}
    return render(request, 'school/partials.html', context)


def student_video(request):
    videos = Video.objects.filter(Q(course__promotion=request.user.student.promotion) | Q(course__promotion=request.user.student.com_prom))
    courses = Course.objects.filter(
        Q(promotion=request.user.student.promotion) | Q(promotion=request.user.student.com_prom))
    courses = set(courses)

    return render(request, 'school/video_student.html', context={'courses': courses, 'videos': videos, 'activevideo': 'active'})


def student_video_course(request, pk):
    course = Course.objects.get(id=pk)
    videos = Video.objects.filter(course=course)
    courses = Course.objects.filter(
        Q(promotion=request.user.student.promotion) | Q(promotion=request.user.student.com_prom))
    courses = set(courses)

    return render(request, 'school/video_student_filter.html', context={'courses': courses, 'course1': course, 'videos': videos, 'activevideo': 'active'})


def clean_view(request):
    return HttpResponse("")


def DownloadView(request, filepath):
    # Open the file for reading conte
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    note = Note.objects.get(id=filepath)
    filepath = BASE_DIR + note.file.url
    filepath.encode()
    print(filepath)
    filename = note.file.name
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response