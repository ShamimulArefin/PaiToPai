from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Create a slug based on the name and user
        if not self.slug:
            # Create a slug from the name and the user's id to ensure uniqueness
            slug_base = slugify(self.name)
            self.slug = f"{slug_base}-{self.user.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + self.user.username

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.amount} - {self.category}"