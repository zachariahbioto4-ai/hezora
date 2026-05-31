from django.db import models
from django.utils.text import slugify
import uuid


class Genre(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    slug  = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self): return self.name


class Author(models.Model):
    name    = models.CharField(max_length=200)
    bio     = models.TextField(blank=True)
    photo   = models.ImageField(
                upload_to='authors/', blank=True, null=True)

    def __str__(self): return self.name


class Book(models.Model):
    # ── identifiers ───────────────────────────────
    id       = models.UUIDField(
                 primary_key=True,
                 default=uuid.uuid4,
                 editable=False)
    title    = models.CharField(max_length=300)
    slug     = models.SlugField(unique=True, blank=True)
    isbn     = models.CharField(
                 max_length=20, blank=True, null=True)

    # ── relationships ─────────────────────────────
    authors  = models.ManyToManyField(
                 Author, related_name='books')
    genres   = models.ManyToManyField(
                 Genre, related_name='books')

    # ── metadata ──────────────────────────────────
    synopsis      = models.TextField()
    cover_image   = models.ImageField(upload_to='covers/')
    pages         = models.PositiveIntegerField(blank=True, null=True)
    language      = models.CharField(
                      max_length=50, default='English')
    published_date= models.DateField(blank=True, null=True)

    # ── pricing ───────────────────────────────────
    price         = models.DecimalField(
                      max_digits=8, decimal_places=2)
    is_free       = models.BooleanField(default=False)

    # ── status ────────────────────────────────────
    is_published  = models.BooleanField(default=False)
    is_featured   = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self): return self.title

    class Meta:
        ordering = ['-created_at']


class BookFile(models.Model):
    # one row per format per book
    FORMAT_CHOICES = [
        ('pdf',  'PDF'),
        ('epub', 'EPUB'),
        ('mobi', 'MOBI / AZW3'),
        ('mp3',  'Audiobook MP3'),
    ]
    book        = models.ForeignKey(
                    Book, on_delete=models.CASCADE,
                    related_name='files')
    format      = models.CharField(
                    max_length=10, choices=FORMAT_CHOICES)
    file        = models.FileField(upload_to='book_files/')
    file_size_mb= models.DecimalField(
                    max_digits=6, decimal_places=2,
                    blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} — {self.get_format_display()}"

    class Meta:
        unique_together = ['book', 'format']
        # one PDF, one EPUB etc. per book


