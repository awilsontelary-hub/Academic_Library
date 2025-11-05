"""
User account models including custom user and institutional ID verification.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class InstitutionalID(models.Model):
    """
    Pre-approved institutional IDs for registration verification.
    
    This model stores institutional IDs (student/employee IDs) that can be used
    for verified registration. Each ID can only be used once and has various
    states (active, used, expired, revoked).
    """
    
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
        blank=True,
        help_text="Unique institutional ID (e.g., student ID, employee ID). Leave blank to auto-generate."
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
        """String representation of the institutional ID."""
        return f"{self.institutional_id} ({self.get_account_type_display()})"
    
    @property
    def is_available(self):
        """
        Check if this ID is available for registration.
        
        Returns:
            bool: True if ID is active and not expired, False otherwise
        """
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
    
    @property
    def full_name(self):
        """
        Get the full name if available.
        
        Returns:
            str or None: Full name if both first and last names exist
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None
    
    def mark_as_used(self, user):
        """
        Mark this ID as used by a specific user.
        
        Args:
            user: The User instance that used this institutional ID
        """
        self.status = 'used'
        self.used_at = timezone.now()
        self.used_by = user
        self.save()
    
    def is_expired(self):
        """
        Check if this ID has expired.
        
        Returns:
            bool: True if expires_at is set and in the past
        """
        if self.expires_at:
            return self.expires_at < timezone.now()
        return False


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Adds support for student/staff roles, academic information,
    and linkage to institutional IDs.
    """
    
    staff = models.BooleanField(default=False, help_text="Faculty or staff member")
    student = models.BooleanField(default=False, help_text="Student account")
    academic_level = models.CharField(max_length=32, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Link to institutional ID used during registration
    institutional_id = models.OneToOneField(
        InstitutionalID,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The institutional ID used during registration"
    )

    def __str__(self):
        """String representation of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def full_name(self):
        """
        Get the user's full name or username as fallback.
        
        Returns:
            str: Full name or username
        """
        return f"{self.first_name} {self.last_name}".strip() or self.username

