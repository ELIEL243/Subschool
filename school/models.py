import datetime
from django.contrib.auth.models import User
from slugify import slugify
from django.db import models

# Create your models here.

level = (('0', '0'),
         ('1', '1'),
         ('2', '2'),
         ('3', '3'),
         ('4', '4'),)

type_dutty = (
    ('TP', 'TP'),
    ('TD', 'TD'),
    ('INTERROGATION', 'INTERROGATION'),
    ('EXAMEN', 'EXAMEN'),
)

owner_types = (
    ('1', 'professeur'),
    ('2', 'etudiant'),
)


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    level = models.CharField(choices=level, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name += " " + self.faculty.name
        super(Promotion, self).save(*args, **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    matricule = models.CharField(max_length=255, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    com_prom = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True, related_name="complement")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.matricule = slugify(self.promotion.name) + str(datetime.datetime.now().timestamp())
        #self.promotion = Promotion.objects.get(level=self.promotion.level)
        super(Student, self).save(*args, **kwargs)


class Note(models.Model):
    file = models.FileField(null=True, upload_to="course_notes")

    def __str__(self):
        return self.file.name


class Course(models.Model):
    image = models.FileField(upload_to="course_img", null=True)
    name = models.CharField(max_length=255)
    promotion = models.ManyToManyField(Promotion, related_name="courses")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    credit = models.IntegerField(default=1)
    description = models.TextField(null=True)
    note = models.ManyToManyField(Note, related_name="note")
    hours = models.IntegerField()

    def __str__(self):
        return self.name


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="video_course")

    def __str__(self):
        return self.title


class HomeWork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    file = models.FileField(null=True, upload_to="homeworks")
    date = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    notice = models.TextField(blank=True)
    cote = models.IntegerField()
    completed = models.BooleanField(default=False)
    type = models.CharField(choices=type_dutty, max_length=255, null=True)

    def __str__(self):
        return str(self.id)


class Submission(models.Model):
    homework = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submission", null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    comment = models.TextField(null=True)
    coted = models.BooleanField(null=True, default=False)
    cote = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.id)

    @property
    def test_status(self):
        if self.date > self.homework.end:
            return True
        return False


class Grade(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Question(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    question = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    satisfied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name}: {self.question}"

    @property
    def get_nbr_response_student(self):
        responses = Response.objects.filter(question=self, is_read=False)
        nbr_r = 0
        for response in responses:
            if response.owner_type != "2":
                nbr_r += 1
        return nbr_r

    @property
    def get_nbr_response_teacher(self):
        responses = Response.objects.filter(question=self, is_read=False)
        nbr_r = 0
        for response in responses:
            if response.owner_type != "1":
                nbr_r += 1
        return nbr_r


class Response(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    owner_type = models.CharField(max_length=255, choices=owner_types)
    response = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.response
