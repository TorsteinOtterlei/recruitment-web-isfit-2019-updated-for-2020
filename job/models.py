from django.db import models


class Job(models.Model):
    job_title = models.CharField(max_length=100)
    gang = models.CharField(max_length=100)

    def __str__(self):
        return str(self.job_title) + ', ' + str(self.gang)

class Job_Detail(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    head_of_gang = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.description

class Applicant(models.Model):
    first_name = models.CharField(default='', max_length=100)
    last_name = models.CharField(default='', max_length=100)
    phone_number = models.IntegerField(default=0)
    email = models.EmailField(max_length=100)
    lives_in_trondheim = models.BooleanField(default=False)

    def __str__(self):
        return str(self.last_name) + ', ' + str(self.first_name)

class Application(models.Model):
    applicant = models.ManyToManyField(Applicant)
    applying_for = models.ManyToManyField(Job)
    application_text = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.applicant)+': '+str(self.applying_for)

