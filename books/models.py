from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

class Book(models.Model):
    title = models.CharField(max_length=255, help_text="The title of the book")
    author = models.CharField(max_length=255, blank=True, default="Unknown Author")
    cover_image = CloudinaryField('image', blank=True, null=True)
    cover_url = models.URLField(max_length=500, blank=True, null=True, help_text="Fallback cover URL if no upload")
    category = models.CharField(max_length=100, default="General")

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=4.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    pages = models.PositiveIntegerField(default=200)
    ratings_count = models.CharField(max_length=50, default="0")
    reviews_count = models.CharField(max_length=50, default="0")

    is_recommended = models.BooleanField(default=False)
    color_gradient = models.CharField(
        max_length=100,
        default="from-slate-700 to-slate-900",
        help_text="Tailwind CSS gradient classes"
    )
    description = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_cover(self):
        """Returns Cloudinary URL if uploaded, else falls back to cover_url"""
        if self.cover_image:
            return self.cover_image.url
        return self.cover_url or 'https://via.placeholder.com/300x400?text=No+Cover'


class BookFile(models.Model):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
        ('mobi', 'MOBI'),
        ('mp3', 'Audiobook MP3'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    file = CloudinaryField(
        'raw',
        resource_type='raw',
        blank=True,
        null=True,
        help_text="Upload PDF, EPUB, or MOBI file"
    )
    file_url = models.URLField(max_length=500, blank=True, null=True, help_text="External URL fallback")
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    file_size_mb = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} — {self.get_file_format_display()}"

    def get_download_url(self):
        """Returns Cloudinary URL if uploaded, else fallback URL"""
        if self.file:
            return self.file.url
        return self.file_url or ''

    class Meta:
        unique_together = ['book', 'file_format']
