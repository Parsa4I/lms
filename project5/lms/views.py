from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
import mimetypes
from datetime import date, datetime
from .forms import *
from .models import *


# main page
def index(request):
    return render(request, 'lms/index.html')


# create a new course by teachers or add a course by students
def new_course(request):
    if request.method == 'POST':
        # teacher user
        if request.user.is_teacher:
            # Create a private/public course
            course_name = request.POST['course-name']
            is_private = request.POST.get('course-type', 'off')
            newcourse = Course(course_name=course_name, teacher=request.user)
            if is_private == 'on':
                newcourse.is_private = True
                course_password = request.POST['course-password']
                newcourse.course_password = course_password
            newcourse.save()
            request.user.teacher_courses.add(newcourse)
            return HttpResponseRedirect(f'/course/{newcourse.pk}')
        # student user
        else:
            course_id = int(request.POST['course-id'])-1000
            course_password = request.POST['course-password']

            # if user entered a password:
            if course_password != '':
                # if a course with the entered id existed
                try:
                    newcourse = Course.objects.get(pk=course_id)
                    # check if the course requires a password
                    if newcourse.course_password != None:
                        # if it did, compare the passwords
                        if newcourse.course_password == course_password:
                            request.user.student_courses.add(newcourse)
                            return HttpResponseRedirect(f'/course/{course_id}')
                        else:
                            return render(request, 'lms/new-course.html', {
                                'message': 'Invalid id and/or password.'
                            })
                    # if the course didn't have a password, let the user in
                    else:
                        request.user.student_courses.add(newcourse)
                        return HttpResponseRedirect(f'/course/{course_id}')
                except:
                    return render(request, 'lms/new-course.html', {
                        'message': 'Invalid id and/or password.'
                    })
            # if user didn't enter any password
            else:
                try:
                    # try finding a course with the entered id
                    newcourse = Course.objects.get(pk=course_id)
                    # if the course doesn't require a password, let the user in
                    if newcourse.course_password is None:
                        request.user.student_courses.add(newcourse)
                        return HttpResponseRedirect(f'/course/{course_id}')
                    else:
                        return render(request, 'lms/new-course.html', {
                            'message': 'This course requires a password.'
                        })
                except:
                    return render(request, 'lms/new-course.html', {
                        'message': 'Invalid id and/or password.'
                    })
    else:
        return render(request, 'lms/new-course.html')


# return course template
def course_view(request, course_id):
    mycourse = get_object_or_404(Course, pk=course_id)
    return render(request, 'lms/course.html', {
        'course_id': mycourse.course_id,
        'course_name': mycourse.course_name,
        'teacher': mycourse.teacher.username,
        'students': [student.username for student in mycourse.students.all()],
        'course': mycourse
    })


def signup_in_course(request, course_id):
    return render(request, 'lms/new-course.html', {
        'default_id': course_id
    })


# return a user's information
def user_view(request, username):
    user = get_object_or_404(User, username=username)
    return JsonResponse(user.serialize())


# return a template containing a user's info
def user_template(request, username):
    user = User.objects.get(username=username)
    if user.is_teacher:
        return render(request, 'lms/user.html', {
            'username': user.username,
            'role': 'teacher'
        })
    else:
        return render(request, 'lms/user.html', {
            'username': user.username,
            'role': 'student'
        })


# return a json response containing courses of a specific user
def courses(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_teacher:
        all_courses = user.teacher_courses.all()
        all_courses = all_courses.order_by('course_name')
        return JsonResponse([a_course.serialize() for a_course in all_courses], safe=False)
    else:
        all_courses = user.student_courses.all()
        all_courses = all_courses.order_by('course_name')
        return JsonResponse([a_course.serialize() for a_course in all_courses], safe=False)


# return a json reponse containing homeworks related to a course
def course_homework(request, course_id):
    the_course = Course.objects.get(pk=course_id)
    homeworks = Homework.objects.filter(course=the_course)
    homeworks = homeworks.order_by('due_date')
    return JsonResponse([ahomework.serialize() for ahomework in homeworks], safe=False)


# return a homework template
def homework(request, hw_id):
    myhomework = Homework.objects.get(pk=hw_id)
    hw_form = Submit_Homework()
    fname = myhomework.file.name
    userhomeworks = UserHomework.objects.filter(homework=myhomework)
    userhomeworks = userhomeworks.order_by('-score')
    is_past_due = False
    if date.today() > myhomework.due_date:
        is_past_due = True
    elif date.today() == myhomework.due_date and datetime.now().time() > myhomework.due_time:
        is_past_due = True

    if request.user.is_teacher:
        return render(request, 'lms/homework.html', {
            'id': myhomework.pk,
            'title': myhomework.title,
            'description': myhomework.description,
            'duedate': myhomework.due_date,
            'duetime': myhomework.due_time,
            'fname': fname,
            'userhomeworks': userhomeworks,
            'len': len(userhomeworks),
            'form': hw_form,
        })
    else:
        done_hw = False
        if request.user in myhomework.students.all():
            done_hw = True
        try:
            userhw = UserHomework.objects.get(student=request.user, homework=myhomework)
            return render(request, 'lms/homework.html', {
                'id': myhomework.pk,
                'title': myhomework.title,
                'description': myhomework.description,
                'duedate': myhomework.due_date,
                'duetime': myhomework.due_time,
                'fname': fname,
                'done_hw': done_hw,
                'upload_date': userhw.upload_date,
                'upload_time': userhw.upload_time,
                'is_past_due': is_past_due,
                'score': userhw.score,
                'userhomeworks': userhomeworks,
                'len': len(userhomeworks),
                'form': hw_form,
            })
        except:
            return render(request, 'lms/homework.html', {
                'id': myhomework.pk,
                'title': myhomework.title,
                'description': myhomework.description,
                'duedate': myhomework.due_date,
                'duetime': myhomework.due_time,
                'is_past_due': is_past_due,
                'fname': fname,
                'done_hw': done_hw,
                'userhomeworks': userhomeworks,
                'len': len(userhomeworks),
                'form': hw_form,
            })


# add a new homework
def add_homework(request, course_id):
    course = get_object_or_404(Course, pk=course_id-1000)
    if request.method == 'GET':
        form = Add_Homework_Form()
        return render(request, 'lms/add-homework.html', {
            'course_id': course.course_id,
            'course_name': course.course_name,
            'form': form
        })
    else:
        new_homework = Homework.objects.create(course=course, title=request.POST['title'],
            description=request.POST['description'], due_date=request.POST['due_date'],
            due_time=request.POST['due_time'], file=request.FILES['desc_file'])

        return HttpResponseRedirect(f'/homework/{new_homework.pk}')


# submit homework by student
def submit_homework(request, hw_id):
    myhomework = Homework.objects.get(pk=hw_id)
    file = request.FILES['homework_file']
    UserHomework.objects.create(student=request.user, homework=myhomework,
        upload_time=datetime.now(), upload_date=datetime.today(), file=file)
    return HttpResponseRedirect(f'/homework/{myhomework.pk}')


# download a file
def download(request, fname):
    filepath = fname
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % fname
    return response


# return a json containing submited homework by students for a certain homework
def submited_homework(request, hw_id):
    myhomework = Homework.objects.get(pk=hw_id)
    submited = UserHomework.objects.filter(homework=myhomework, score=None)
    return JsonResponse([shw.serialize() for shw in submited], safe=False)


# return a template for teacher to give a score to a submitted homework
def give_score(request, userhw_id):
    userhw = UserHomework.objects.get(pk=userhw_id)
    if request.method == 'POST':
        score = request.POST['score']
        userhw.score = score
        userhw.save()
        return HttpResponseRedirect(f'/homework/{userhw.homework.pk}')
    else:
        form = Give_Score()
        return render(request, 'lms/give-score.html', {
            'pk': userhw_id,
            'student': userhw.student.username,
            'homework': userhw.homework.title,
            'form': form,
        })


# return a json for undone homeworks
def index_homeworks(request):
    homeworks = Homework.objects.filter(course__students=request.user)
    homeworks = homeworks.order_by('due_date', 'due_time')
    not_done_hw = []
    for hw in homeworks:
        if request.user not in hw.students.all():
            not_done_hw.append(hw)

    final_hw_list=[]
    for hw in not_done_hw:
        if date.today() < hw.due_date:
            final_hw_list.append(hw.serialize())
        elif date.today() == hw.due_date and datetime.now().time() < hw.due_time:
            final_hw_list.append(hw.serialize())

    return JsonResponse(final_hw_list, safe=False)


# return course search template
def find_public_courses(request):
    return render(request, 'lms/find-public-courses.html')


def public_courses(request, a):
    courses = Course.objects.filter(course_name__contains=a, is_private=False)
    return JsonResponse([course.serialize() for course in courses], safe=False)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'lms/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'lms/login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        is_teacher = True if request.POST['role'] == 'teacher' else False

        if password != confirmation:
            return render(request, 'lms/signup.html', {
                'message': 'Passwords must match.'
            })
        else:
            try:
                user = User.objects.create_user(username=username, password=password, email=email, is_teacher=is_teacher)
                user.save()
                login(request, user)
            except IntegrityError:
                return render(request, 'lms/signup.html', {
                    'message': 'Username already taken.'
                })
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'lms/signup.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
