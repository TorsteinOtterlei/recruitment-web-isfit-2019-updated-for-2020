from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


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
    email = models.EmailField(max_length=200)
    #name_of_interviewer = models.CharField(max_length=100)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return str(self.title) + ', ' + str(self.gang)
