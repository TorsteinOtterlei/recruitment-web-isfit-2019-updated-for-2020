from django.db import models
import math
from accounts.models import User
# local

# other apps
#from accounts.models import User

def makeDates(numb):
    return ",".join([str(i) for i in range(numb)])

class Section(models.Model):
    name = models.CharField(max_length=100)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    information = models.TextField(max_length=20000)

    class Meta:
        verbose_name = "section"
        verbose_name_plural = "sections"
        ordering = ['name']

    def __str__(self):
        if self.name == None:
            return 'error'
        return self.name

class Gang(models.Model):
    name = models.CharField(max_length=100)
    #leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name="gangs")

    class Meta:
        verbose_name = "gang"
        verbose_name_plural = "gangs"
        order_with_respect_to = 'section'

    def __str__(self):
        if self.name == None:
            return 'error'
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    gang = models.ForeignKey(Gang, on_delete=models.SET_NULL, null=True, related_name="projects")

    def __str__(self):
        if self.name == None:
            return 'error'
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)
    gang = models.ForeignKey(Gang, on_delete=models.SET_NULL, null=True, related_name="positions")
    description = models.TextField(max_length=20000)
    interviewers = models.ManyToManyField(User, related_name="positions", blank=True)
    contact_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="position", blank=True)
    comment = models.TextField(max_length=100, default='', blank=True)

    class Meta:
        verbose_name = "position"
        verbose_name_plural = "positions"
        order_with_respect_to = "gang"

    def __str__(self):
        if self.title == None or self.gang == None:
            return 'error'
        return "{} ({})".format(self.title, self.gang)

    def get_contact_person(self):
        return self.contact_person

class Date(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="date")
    dates = models.TextField(max_length=2000, default=makeDates(182), blank=True)

    class Meta:
        verbose_name = "date"
        verbose_name_plural = "dates"

    def __str__(self):
        if self.user.email == None:
            return 'error'
        return "Dates for {}".format(self.user.email)

    def dates_list(self):
        return [int(x) for x in self.dates.split(',') if x != ""]

    def set_dates(self, list):
        if (type(list) == type([])):
            self.dates = ",".join([str(x) for x in list])
            self.save()

    def add_time(self, time):
        try:
            time = int(time) # Check that time is actually an int
            self.dates += ',' + str(time)
            self.save()
        except:
            print('Error: adding an invalid time')

    def remove_time(self, time):
        tmp = self.dates.split(',')
        if time in tmp:
            tmp.remove(time)
        self.dates = ",".join(tmp)
        self.save()

    def pretty_dates_list(self):        # NOT TESTED
        if self.dates == '':
            return 'none'
        dates_range = 182
        all_times = ["08:15 - 09:00", "09:15 - 10:00", "10:15 - 11:00",
        "11:15 - 12:00", "12:15 - 13:00", "13:15 - 14:00", "14:15 - 15:00",
        "15:15 - 16:00", "16:15 - 17:00", "17:15 - 18:00", "18:15 - 19:00",
        "19:15 - 20:00", "20:15 - 21:00"]
        all_days = ["Monday 27 Aug", "Tuesday 28 Aug", "Wednesday 29 Aug",
         "Thursday 30 Aug", "Friday 31 Aug", "Saturday 1 Sept", "Sunday 2 Sept",
         "Monday 3 Sept", "Tuesday 4 Sept", "Wednesday 5 Sept", "Thursday 6 Sept",
         "Friday 7 Sept", "Saturday 8 Sept", "Sunday 9 Sept"]

        res = []
        for date in self.dates:
            tmp = float(date)
            if int(tmp) < dates_range//2:
                res.append((first_week[int(tmp)%7] + ' - ' + all_times[int(math.trunc(tmp/7))]))
            else:
                tmp -= dates_range//2
                res.append((second_week[int(tmp)%7] + ' - ' + all_times[int(math.trunc(tmp/7))]))
        return res


class Calendar(models.Model): # NOT IN USE
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

class Interview(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, related_name='interview')
    interviewers = models.ManyToManyField(User, blank=True, related_name='interviews')
    first = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='first_interviews')
    second = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='second_interviews')
    third = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='third_interviews')
    room = models.CharField(max_length=40, default="")
    time = models.IntegerField(default=-1)


    def set_interview_time(self, time):
        if time == 'none':
            self.time = -1
            self.save()
        else:
            self.time = int(time)
            self.save()

    def get_interview_time(self):
        if self.time == -1:
            return 'none'
        return str(self.time)

    def pretty_interview_time(self):
        if self.get_interview_time() == 'none':
            return 'none'
        dates_range = 182
        all_times = ["08:15 - 09:00", "09:15 - 10:00", "10:15 - 11:00",
        "11:15 - 12:00", "12:15 - 13:00", "13:15 - 14:00", "14:15 - 15:00",
        "15:15 - 16:00", "16:15 - 17:00", "17:15 - 18:00", "18:15 - 19:00",
        "19:15 - 20:00", "20:15 - 21:00"]
        first_week = ["Monday 27 Aug", "Tuesday 28 Aug", "Wednesday 29 Aug",
         "Thursday 30 Aug", "Friday 31 Aug", "Saturday 1 Sept", "Sunday 2 Sept"]
        second_week = ["Monday 3 Sept", "Tuesday 4 Sept", "Wednesday 5 Sept", "Thursday 6 Sept",
         "Friday 7 Sept", "Saturday 8 Sept", "Sunday 9 Sept"]

        tmp = float(self.get_interview_time())
        if int(tmp) < dates_range//2:
            return(first_week[int(tmp)%7] + ' - ' + all_times[int(math.trunc(tmp/7))])
        else:
            tmp -= dates_range//2
            return(second_week[int(tmp)%7] + ' - ' + all_times[int(math.trunc(tmp/7))])

    def __str__(self):
        return str(self.room) + ', ' + str(self.pretty_interview_time())
