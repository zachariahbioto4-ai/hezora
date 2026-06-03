from django.db import models
from accounts.models import User
from books.models import Book

class LibraryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user} - {self.book}'
