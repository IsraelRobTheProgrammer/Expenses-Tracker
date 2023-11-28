from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    desc = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Incomes"


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

