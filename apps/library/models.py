from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name

class BookDetails(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_books')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Book Details"
        verbose_name_plural = "Book Details"

    def __str__(self):
        return self.title

class BookFile(models.Model):
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(
        upload_to='books/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Book Files"
        verbose_name_plural = "Book Files"

    def __str__(self):
        return f"{self.book.title} - {self.file.name}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

class Recommendation(models.Model):
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE, related_name='recommendations')
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} recommended by {self.recommended_by.username}"

class BookBorrow(models.Model):
    BORROW_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE, related_name='borrows')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=BORROW_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_borrows')
    
    class Meta:
        ordering = ['-borrowed_date']
    
    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.full_name}"
    
    @property
    def is_overdue(self):
        return self.status == 'approved' and timezone.now() > self.due_date and not self.return_date
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)  # 2 weeks default
        super().save(*args, **kwargs)

class BookReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['book', 'reviewer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.book.title} - {self.rating} stars by {self.reviewer.full_name}"

class BookDownload(models.Model):
    """Track book file downloads for statistics"""
    book_file = models.ForeignKey(BookFile, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-downloaded_at']
        verbose_name = "Book Download"
        verbose_name_plural = "Book Downloads"
    
    def __str__(self):
        return f"{self.book_file.book.title} downloaded by {self.user.full_name} on {self.downloaded_at}"
