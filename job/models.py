from django.db import models
from django.contrib.auth.models import User

class Gang(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=50)
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.title) + ', ' + str(self.gang)

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    phone_number = models.IntegerField()
    #interview_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.applicant)
