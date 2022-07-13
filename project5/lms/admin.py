from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'is_teacher')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'course_id', 'course_name', 'is_private', 'course_password')


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course', 'get_desc', 'due_date', 'due_time')


class UserHomeworkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'file', 'student', 'homework', 'upload_date', 'upload_time', 'score')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(UserHomework, UserHomeworkAdmin)
