from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


class Expenses(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    desc = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Expenses"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
