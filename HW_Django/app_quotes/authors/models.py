from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False)
    born_date = models.CharField(max_length=50)
    born_loc = models.CharField(max_length=50)
    biography = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Quote(models.Model):
    quote = models.CharField(max_length=1000, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
