from django.db import models
from django.utils import timezone
from jobs.models import Position
from accounts.models import User
import math

# Create your models here.
class Application(models.Model):
    first = models.ForeignKey(Position, on_delete=models.SET_NULL, default=None, null=True, related_name="first")
    second = models.ForeignKey(Position, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="second")
    third = models.ForeignKey(Position, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="third")
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, related_name="application")
    text = models.TextField(max_length=2000)
    interview_time = models.IntegerField(default=-1)

    # Shitty quickfix backup fix
    def get_order_time(self):
        if self.interview_time == -1:
            return 99999
        if self.interview_time > 90:
            return 1000 + self.interview_time + (self.interview_time % 7) * 100
        return self.interview_time + (self.interview_time % 7) * 100

    def get_interview_time(self):
        if self.interview_time == -1:
            return 'none'
        return str(self.interview_time)

    def set_interview_time(self, time):
        if time == 'none':
            self.interview_time = -1
            self.save()
        else:
            self.interview_time = int(time)
            self.save()

    def get_positions(self):
        positions = [self.first, self.second, self.third]
        return [pos for pos in positions if pos != None]

    def set_positions(self, positions):
        if positions[0] == '':
            return
        self.second = None
        self.third = None

        self.first = Position.objects.get(title = positions[0])
        if len(positions) > 1:
            self.second = Position.objects.get(title = positions[1])
        if len(positions) > 2:
            self.third = Position.objects.get(title = positions[2])
        self.save()

    def has_positions(self):
        return self.get_positions() != []

    def get_position_gangs(self):
        positions = [self.first, self.second, self.third]
        return [pos.gang.name for pos in positions if pos != None]

    def get_position_sections(self):
        positions = [self.first, self.second, self.third]
        return [pos.gang.section.name for pos in positions if pos != None]


    def pretty_interview_time(self):
        if self.get_interview_time() == 'none':
            return 'none'
        dates_range = 364
        all_times = ["08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30",
        "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30",
        "11:30 - 12:00", "12:00 - 12:30", "12:30 - 13:00", "13:00 - 13:30",
        "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30", "15:30 - 16:00", "16:00 - 16:30", "16:30 - 17:00",
        "17:00 - 17:30", "17:30 - 18:00", "18:00 - 18:30", "18:30 - 19:00", "19:00 - 19:30", "19:30 - 20:00", "20:00 - 20:30", "20:30 - 21:00"]
        first_week = ["Monday 15 Oct", "Tuesday 16 Oct", "Wednesday 17 Oct", "Thursday 18 Oct", "Friday 19 Oct", "Saturday 20 Oct",
         "Sunday 21 Oct"]
        second_week = ["Monday 22 Oct", "Tuesday 23 Oct", "Wednesday 24 Oct", "Thursday 25 Oct",
         "Friday 26 Oct", "Saturday 27 Oct", "Sunday 28 Oct"]

        tmp = float(self.get_interview_time())
        if int(tmp) < dates_range//2:
            return(first_week[int(tmp)%7] + ' - ' + all_times[int(math.trunc(tmp/7))])
        else:
            tmp -= dates_range//2
            return(second_week[int(tmp)%7] + ' - ' + all_times[int(math.trunc(tmp/7))])


    def __str__(self):
        if self.applicant.get_full_name() == None:
            return "error"
        interview_date = self.pretty_interview_time()
        return "{}, Interview: {}".format(self.applicant.get_full_name(), interview_date)
