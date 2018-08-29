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
        if self.applicant.get_full_name() == None:
            return "error"
        interview_date = self.pretty_interview_time()
        return "{}, Interview: {}".format(self.applicant.get_full_name(), interview_date)
