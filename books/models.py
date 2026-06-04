from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255, help_text="The title of the book")
    author = models.CharField(max_length=255, blank=True, default="Unknown Author")
    cover_url = models.URLField(max_length=500, help_text="Direct link to a book cover image")
    category = models.CharField(max_length=100, default="General")
    
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=4.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    pages = models.PositiveIntegerField(default=200)
    ratings_count = models.CharField(max_length=50, default="0", help_text="Formatted ratings (e.g. 1,240)")
    reviews_count = models.CharField(max_length=50, default="0", help_text="Formatted reviews (e.g. 320)")
    
    is_recommended = models.BooleanField(default=False)
    color_gradient = models.CharField(
        max_length=100, 
        default="from-slate-700 to-slate-900", 
        help_text="Tailwind CSS gradient classes (e.g., from-emerald-800 to-teal-900)"
    )
    description = models.TextField(blank=True, default="")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BookFile(models.Model):
    """
    Represents downloadable formats of a book (PDF, EPUB, etc.)
    used by delivery, download, and library apps.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='books/files/', blank=True, null=True)
    file_url = models.URLField(max_length=500, blank=True, null=True, help_text="External URL if hosted outside storage")
    file_format = models.CharField(max_length=10, default="pdf", help_text="e.g. pdf, epub, mobi, mp3")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.file_format.upper()}"
