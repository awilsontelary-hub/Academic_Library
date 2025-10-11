from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class InstitutionalID(models.Model):
    """Model to store pre-approved institutional IDs for registration verification"""
    
    ACCOUNT_TYPES = [
        ('student', 'Student'),
        ('staff', 'Staff/Faculty'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    
    ACADEMIC_LEVELS = [
        ('freshman', 'Freshman'),
        ('sophomore', 'Sophomore'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('graduate', 'Graduate Student'),
        ('phd', 'PhD Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    ]
    
    # Core fields
    institutional_id = models.CharField(
        max_length=20, 
        unique=True, 
        help_text="Unique institutional ID (e.g., student ID, employee ID)"
    )
    account_type = models.CharField(
        max_length=10, 
        choices=ACCOUNT_TYPES,
        help_text="Type of account this ID is authorized for"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        help_text="Current status of this institutional ID"
    )
    
    # Personal information (optional - for pre-population)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    academic_level = models.CharField(
        max_length=20, 
        choices=ACADEMIC_LEVELS, 
        blank=True, 
        null=True
    )
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Optional expiration date for this ID"
    )
    used_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="When this ID was used for registration"
    )
    used_by = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        help_text="User who registered with this ID"
    )
    
    # Administrative fields
    added_by = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='added_institutional_ids',
        help_text="Admin who added this ID"
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Internal notes about this ID"
    )
    
    class Meta:
        verbose_name = "Institutional ID"
        verbose_name_plural = "Institutional IDs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['institutional_id']),
            models.Index(fields=['status']),
            models.Index(fields=['account_type']),
        ]
    
    def __str__(self):
        return f"{self.institutional_id} ({self.get_account_type_display()})"
    
    @property
    def is_available(self):
        """Check if this ID is available for registration"""
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
    
    @property
    def full_name(self):
        """Get the full name if available"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None
    
    def mark_as_used(self, user):
        """Mark this ID as used by a specific user"""
        self.status = 'used'
        self.used_at = timezone.now()
        self.used_by = user
        self.save()
    
    def is_expired(self):
        """Check if this ID has expired"""
        if self.expires_at:
            return self.expires_at < timezone.now()
        return False

class User(AbstractUser):
    staff = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    academic_level = models.CharField(max_length=32, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # New field to link to institutional ID
    institutional_id = models.OneToOneField(
        InstitutionalID,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The institutional ID used during registration"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
 
