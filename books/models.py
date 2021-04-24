from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    publisher = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    location = models.TextField()
    available = models.BooleanField(default=True)
    ISBN = models.CharField(max_length=17)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

class request_detail(models.Model):
    book_detail = models.ForeignKey(Book, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    return_date = models.DateField(default=timezone.now()+datetime.timedelta(days=7))
    request_status = models.CharField(max_length=15, default = 'Pending')

    def __str__(self):
        return self.book_detail.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.book_detail.pk})