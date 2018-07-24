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


class Ranking(models.Model):
    first = models.ForeignKey(Position, related_name='first' , on_delete=models.CASCADE)
    second = models.ForeignKey(Position, related_name='second' ,  on_delete=models.CASCADE, default=None, null=True)
    third = models.ForeignKey(Position, related_name='third' ,  on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        s = "1. " + str(self.first.title)
        if self.second != None:
            s += ", 2. " + str(self.second.title)
        if self.third != None:
            s += ", 3. " + str(self.third.title)
        return s


class Application(models.Model):
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE, default=None, null=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    phone_number = models.CharField(max_length=12)
    interview_time = models.DateTimeField(null=True, blank=True, default=None)

    # IDEA: Remove ranking, add here
    #first = models.ForeignKey(Position, related_name='first' , on_delete=models.CASCADE)
    #second = models.ForeignKey(Position, related_name='second' ,  on_delete=models.CASCADE, default=None, null=True)
    #third = models.ForeignKey(Position, related_name='third' ,  on_delete=models.CASCADE, default=None, null=True)

    def pretty_date(self):
        if self.interview_time != None:
            return self.interview_time.strftime('%a %b %Y %H:%M') # day month year hour:min
        else:
            return "No time set"

    def __str__(self):
        lastname = str(self.applicant.last_name)
        firstname = str(self.applicant.first_name)
        interview_date = self.pretty_date()
        return "{}, {}, Date: {}".format(lastname, firstname, interview_date)


class Dates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dates = models.TextField(max_length=2000, default="", blank=True) # 1,2,43,68 possible dates

    def dates_list(self):
        if dates == None:
            return [i for i in range(70)]
        else:
            return [int(x) for x in self.dates.split(',')]

    def __str__(self):
        return self.user.username + " " + self.dates


class Calendar(models.Model):
    gangleader = models.ForeignKey(User, on_delete=models.CASCADE)
    dict = models.TextField(max_length=2000, default=None) # user:1,user:2
    #gangleader_dates = models.ForeignKey(Dates, on_delete=models.CASCADE, default=None, null=True)

    def calendar_dict(self):
        c = dict.split(",")
        cal = {}
        for tuple in c:
            t = tuple.split(":")
            cal[t[0]] = int(t[1])
        return cal

    def __str__(self):
        return "Calendar for " + self.gangleader
