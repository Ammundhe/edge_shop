from unicodedata import category
from django.db import models

class BlogCategory(models.Model):
    name=models.CharField(max_length=155)
    status=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name)

class BlogPost(models.Model):
    category=models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="BlogPost")
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    description=models.TextField()
    cover_image=models.ImageField()
    date=models.DateField()

    def __str__(self) -> str:
        return str(self.title)