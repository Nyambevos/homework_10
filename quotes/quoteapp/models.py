from django.db import models

# Create your models here.

class Authors(models.Model):
    fullname = models.CharField(max_length=50, null=False, unique=True)
    born_date = models.CharField(max_length=30)
    born_location = models.CharField(max_length=80)
    description = models.CharField()

    def __str__(self):
        return f"{self.fullname}"