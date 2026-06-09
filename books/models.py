from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=14.99)
    stock = models.PositiveIntegerField(default=10)
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_cover(self):
        """Return book cover URL or default image"""
        if self.image:
            return self.image.url
        return '/static/images/default-book-cover.jpg'  # You can change this later

    @property
    def display_price(self):
        return f"${self.price:.2f}"

# BookFile for digital downloads
class BookFile(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='file')
    file = models.FileField(upload_to='book_files/')
    format = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('epub', 'EPUB')], default='pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.format}"
