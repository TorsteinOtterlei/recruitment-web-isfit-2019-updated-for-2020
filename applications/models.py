from django.db import models
from django.utils import timezone
from jobs.models import Position
from accounts.models import User

# Create your models here.
class Application(models.Model):
    first = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, related_name="first")
    second = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="second")
    third = models.ForeignKey(Position, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="third")
    applicant = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    interview_time = models.DateTimeField(null=True, blank=True, default=None)
    dates = models.TextField(max_length=2000, default="", blank=True) # 1,2,43,68 possible dates

    def dates_list(self):
        print(self.dates)
        print("=====================")
        print(int(x) for x in self.dates.split(',') if x != "")
        return [int(x) for x in self.dates.split(',') if x != ""]

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
