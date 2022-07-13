from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('new-course', views.new_course, name='new_course'),
    path('new-course/<int:course_id>', views.signup_in_course, name='new_course_id'),
    path('course/<int:course_id>', views.course_view, name='course_view'),
    path('homework/<int:hw_id>', views.homework, name='homework'),
    path('give-score/<int:userhw_id>', views.give_score, name='give_score'),
    path('user/<str:username>', views.user_template, name='user'),
    path('find-public-courses', views.find_public_courses, name='find_public_courses'),
    path('course/<int:course_id>/add-homework', views.add_homework, name='add_homework'),
    path('submit-homework/<int:hw_id>', views.submit_homework, name='submit_homework'),

    #API Routes
    path('user-view/<str:username>', views.user_view, name='user_view'),
    path('index-homeworks', views.index_homeworks, name='index_homeworks'),
    path('courses/<str:username>', views.courses, name='courses'),
    path('course/<int:course_id>/homework', views.course_homework, name='course_homework'),
    path('download/<path:fname>', views.download, name='download'),
    path('submited-homework/<int:hw_id>', views.submited_homework, name='submited_homework'),
    path('public-courses/<str:a>', views.public_courses, name='public_courses'),
]