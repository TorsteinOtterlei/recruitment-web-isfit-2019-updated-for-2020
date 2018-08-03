from django.db import models
# local

# other apps
from accounts.models import User


class Section(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    information = models.TextField(max_length=20000)

    def __str__(self):
        return self.name

class Gang(models.Model):
    name = models.CharField(max_length=50)
    #leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="gangs")

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=50)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name="positions")
    description = models.TextField(max_length=20000)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #email = models.EmailField(max_length=200)
    #name_of_interviewer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title) + ', ' + str(self.gang)

class Date(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dates = models.TextField(max_length=2000, default="", blank=True) # 1,2,43,68 possible dates

    def __str__(self):
        return "Dates for {}".format(self.user.email)

    def dates_list(self):
        return [int(x) for x in self.dates.split(',') if x != ""]

class Calendar(models.Model):
    gangleader = models.OneToOneField(User, on_delete=models.CASCADE)
    dict = models.TextField(max_length=2000, default=None) # user:1,user:2
    #gangleader_dates = models.ForeignKey(Dates, on_delete=models.CASCADE, default=None, null=True)

    def calendar_dict(self):
        c = dict.split(",")
        cal = {}
        for tuple in c:
            t = tuple.split(":")
            user = User.objects.get(username=t[0])
            cal[user] = int(t[1])
        return cal

    def __str__(self):
        return "Calendar for " + self.gangleader
