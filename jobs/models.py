from django.db import models
# local

# other apps
from accounts.models import User

def makeDates(numb):
    return ",".join([str(i) for i in range(numb)])

class Section(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    information = models.TextField(max_length=20000)

    def __str__(self):
        if self.name == None:
            return 'error'
        return self.name

class Gang(models.Model):
    name = models.CharField(max_length=50)
    #leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="gangs")

    def __str__(self):
        if self.name == None:
            return 'error'
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        if self.name == None:
            return 'error'
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=50)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE, related_name="positions")
    description = models.TextField(max_length=20000)
    interviewer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="position")
    #email = models.EmailField(max_length=200)
    #name_of_interviewer = models.CharField(max_length=100)

    def __str__(self):
        if self.title == None or self.gang == None:
            return 'error'
        return "{} ({})".format(self.title, self.gang)

class Date(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="date")
    dates = models.TextField(max_length=2000, default=makeDates(140), blank=True) # 1,2,43,68 possible dates

    def __str__(self):
        if self.user.email == None:
            return 'error'
        return "Dates for {}".format(self.user.email)

    def dates_list(self):
        return [int(x) for x in self.dates.split(',') if x != ""]

    # def remove_time(self, time):
    #     tmp = self.dates.split(',')
    #     tmp.remove(time)
    #     self.dates = ",".join(tmp)
    #     self.save()

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
        if self.gangleader == None:
            return 'error'
        return "Calendar for " + self.gangleader
