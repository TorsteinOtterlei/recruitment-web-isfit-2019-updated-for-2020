from django.db import models
from django.utils import timezone
from jobs.models import Position
from accounts.models import User

# Create your models here.
class Application(models.Model):
    first = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, related_name="first")
    second = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="second")
    third = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="third")
    applicant = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    interview_time = models.DateTimeField(null=True, blank=True, default=None)

    def get_positions(self):
        positions = [self.first, self.second, self.third]
        return [pos for pos in positions if pos != None]

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
