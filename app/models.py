
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Book(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('BORROWED', 'Borrowed'),
    )

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description=models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return self.title
    

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"    