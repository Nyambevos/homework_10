from django.db import models

# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False, unique=True)
    born_date = models.CharField(max_length=30)
    born_location = models.CharField(max_length=80)
    description = models.CharField(null=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return f"{self.fullname}"
    
class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(null=False)
    tags =  models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"
