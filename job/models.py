from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Section(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    information = models.TextField(max_length=20000)

    def __str__(self):
        return self.name


class Gang(models.Model):
    name = models.CharField(max_length=50)
    #leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=50)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE)
    description = models.TextField(max_length=20000)
    email = models.EmailField(max_length=200)
    name_of_interviewer = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return str(self.title) + ', ' + str(self.gang)


class Application(models.Model):
    positions = models.ManyToManyField(Position)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    phone_number = models.CharField(max_length=12)
    #weight = models.IntegerField(default=0)
    trondheim = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    interview_time = models.DateTimeField(null=True, blank=True)
    #interview_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        if (self.interview_time == None):
            return str(self.applicant.last_name) + ', ' + str(self.applicant.first_name) + '. No time set'
        else:
            return str(self.applicant.last_name) + ', ' + str(self.applicant.first_name)+ '. Date: ' + \
                   str(self.interview_time.day) + '.' + str(self.interview_time.month) + '.' + str(self.interview_time.year) + '. Time: ' + \
                   str(self.interview_time.hour) + ':' + str(self.interview_time.minute)

class Ranking(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=3,validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ])

    def __str__(self):
        return str(self.applicant.first_name) + ' ' + str(self.applicant.last_name) + ', ' + str(self.position.title) + ' ' + str(self.rank)