import random

from django.db import models
from django.contrib.auth.models import AbstractUser


class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="lorem")
    competitiveness = models.TextField(default="ipsum")

    class Meta:
        ordering = ["name"]
        verbose_name = "topic"
        verbose_name_plural = "topics"

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()
    monthly_expenses = models.IntegerField(default=random.randint(200, 20000))
    monthly_income = models.IntegerField(default=random.randint(200, 20000))

    REQUIRED_FIELDS = ["years_of_experience"]

    class Meta:
        ordering = ["username"]
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ManyToManyField(Topic, related_name="topics")
    publishers = models.ManyToManyField(Redactor, related_name="redactors")

    def __str__(self):
        return f"{self.title} ({self.published_date})"
