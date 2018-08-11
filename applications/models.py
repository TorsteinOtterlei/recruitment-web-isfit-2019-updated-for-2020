from django.db import models
from django.utils import timezone
from jobs.models import Position
from accounts.models import User

# Create your models here.
class Application(models.Model):
    first = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, related_name="first")
    second = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="second")
    third = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="third")
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, related_name="application")
    text = models.TextField(max_length=2000)
    interview_time = models.TextField(max_length=4, default='none')

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

    def has_positions(self):
        return self.get_positions() != []

    def get_position_gangs(self):
        positions = [self.first, self.second, self.third]
        return [pos.gang.name for pos in positions if pos != None]

    def get_position_sections(self):
        positions = [self.first, self.second, self.third]
        return [pos.gang.section.name for pos in positions if pos != None]


    def pretty_date(self):
        if self.interview_time != None:
            return self.interview_time # TODO: FIX
        else:
            return "No time set"

    def __str__(self):
        if self.applicant.get_full_name() == None:
            return "error"
        interview_date = self.pretty_date()
        return "{}, Interview: {}".format(self.applicant.get_full_name(), interview_date)
