from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False, null=False)

    def serialize(self):
        return {
            'pk': self.pk,
            'username': self.username,
            'role': 'teacher' if self.is_teacher else 'student'
        }


class Course(models.Model):
    course_id = models.IntegerField(blank=False)
    course_name = models.CharField(max_length=64, blank=False, null=False)
    is_private = models.BooleanField(default=False, blank=False, null=False)
    course_password = models.CharField(max_length=16, blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_courses')
    students = models.ManyToManyField(User, blank=True, related_name='student_courses')

    @property
    def course_id(self):
        return self.pk + 1000

    def serialize(self):
        return {
            'pk': self.pk,
            'course_id': self.course_id,
            'course_name': self.course_name,
            'is_private': self.is_private,
            'teacher': self.teacher.serialize(),
            'students': [student.serialize() for student in self.students.all()],
            'homeworks': [homework.serialize() for homework in self.course_homeworks.all()],
        }

    def __str__(self):
        return f'{self.course_id}: {self.course_name}'


class Homework(models.Model):
    def upload_path(self, filename):
        return f'./lms/static/lms/uploads/hw_desc/course_{self.course.pk}/hw_{self.pk}/{filename}'

    title = models.CharField(max_length=64, blank=False, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False, related_name='course_homeworks')
    description = models.TextField(null=True, blank=False)
    due_date = models.DateField(null=True, blank=False)
    due_time = models.TimeField(null=True, blank=False)
    file = models.FileField(null=True, blank=True, upload_to=upload_path)
    students = models.ManyToManyField(User, blank=True, related_name='homeworks_done', through='UserHomework')

    def get_desc(self):
        if len(self.description) <= 50:
            return self.description
        return self.description[:50]+'...'

    def serialize(self):
        return {
            'pk': self.pk,
            'title': self.title,
            'description': self.description,
            'duedate': self.due_date.strftime("%B %d, %Y"),
            'duetime': self.due_time.strftime("%H:%M")
        }

    def __str__(self):
        return f'{self.title} | {self.course}'


class UserHomework(models.Model):
    def homework_path(self, filename):
        return f'./lms/static/lms/uploads/hw_submit/course_{self.homework.course.pk}/hw_{self.homework.pk}/st_{self.student.pk}/{filename}'
    
    student = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='uploaded_files')
    homework = models.ForeignKey(Homework, null=True, on_delete=models.CASCADE, related_name='files')
    upload_time = models.TimeField(null=True)
    upload_date = models.DateField(null=True)
    score = models.IntegerField(blank=True, null=True)
    file = models.FileField(null=True, upload_to=homework_path)

    def serialize(self):
        return  {
            'pk': self.pk,
            'student': self.student.serialize(),
            'homework': self.homework.serialize(),
            'upload_time': self.upload_time.strftime('%H:%M'),
            'upload_date': self.upload_date.strftime('%B %d, %Y'),
            'score': self.score,
            'file': self.file.name
        }
