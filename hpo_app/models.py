from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
import uuid


class Organisation(models.Model):
    """Organisation model based on organisationSchema"""
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    PAYMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'


class Admin(models.Model):
    """Admin model based on adminSchema"""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6)])
    
    ROLE_CHOICES = [
        ('Super Admin', 'Super Admin'),
        ('Organization Admin', 'Organization Admin'),
        ('HPO Admin', 'HPO Admin'),
        ('superadmin', 'superadmin'),
        ('orgadmin', 'orgadmin'),
        ('hpoadmin', 'hpoadmin'),
    ]
    role = models.CharField(
        max_length=50, 
        choices=ROLE_CHOICES, 
        default='Organization Admin'
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    
    ACCESS_LEVEL_CHOICES = [
        ('full', 'Full'),
        ('limited', 'Limited'),
        ('read-only', 'Read Only'),
    ]
    access_level = models.CharField(
        max_length=20, 
        choices=ACCESS_LEVEL_CHOICES, 
        default='limited'
    )
    
    supervisor = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    organisation = models.ForeignKey(
        Organisation, 
        on_delete=models.CASCADE, 
        related_name='admins',
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class Group(models.Model):
    """Group model based on groupSchema"""
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    created_by = models.ForeignKey(
        'Player', 
        on_delete=models.CASCADE, 
        related_name='created_groups'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Player(models.Model):
    """Player model based on playerSchema"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6)])
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    gender = models.CharField(
        max_length=20, 
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True
    )
    
    organization = models.ForeignKey(
        Organisation, 
        on_delete=models.CASCADE, 
        related_name='players',
        blank=True, 
        null=True
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        related_name='members',
        blank=True, 
        null=True
    )
    
    SUBSCRIPTION_TYPE_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    subscription_type = models.CharField(
        max_length=20, 
        choices=SUBSCRIPTION_TYPE_CHOICES, 
        default='free'
    )
    
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=255, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    parent_guardian = models.CharField(max_length=255, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    
    EDUCATION_LEVEL_CHOICES = [
        ('elementary', 'Elementary'),
        ('middle_school', 'Middle School'),
        ('high_school', 'High School'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('other', 'Other'),
    ]
    education_level = models.CharField(
        max_length=20, 
        choices=EDUCATION_LEVEL_CHOICES, 
        blank=True, 
        null=True
    )
    
    interests = models.JSONField(default=list, blank=True)  # Array of strings
    notes = models.TextField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    
    # Existing compatibility fields
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    points = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    groups = models.ManyToManyField(Group, related_name='group_members', blank=True)
    
    SUBSCRIPTION_STATUS_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('org_paid', 'Organization Paid'),
    ]
    subscription_status = models.CharField(
        max_length=20, 
        choices=SUBSCRIPTION_STATUS_CHOICES, 
        default='free'
    )
    
    organisation = models.ForeignKey(
        Organisation, 
        on_delete=models.CASCADE, 
        related_name='organisation_players',
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'


class Question(models.Model):
    """Individual question model"""
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('multiple_choice', 'Multiple Choice'),
            ('true_false', 'True/False'),
        ],
        default='multiple_choice'
    )
    
    # Store options as JSON for multiple choice questions
    # For true/false, this will be ['True', 'False']
    options = models.JSONField(default=list, blank=True)
    correct_answer = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=1)
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Automatically set options for true/false questions"""
        if self.question_type == 'true_false':
            self.options = ['True', 'False']
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate question data"""
        from django.core.exceptions import ValidationError
        
        if self.question_type == 'true_false':
            if self.correct_answer and self.correct_answer not in ['True', 'False']:
                raise ValidationError('True/False questions must have correct_answer as "True" or "False"')
        elif self.question_type == 'multiple_choice':
            # Only validate options if they exist (form will handle setting them)
            if self.options and len(self.options) < 2:
                raise ValidationError('Multiple choice questions must have at least 2 options')
            if self.options and self.correct_answer and self.correct_answer not in self.options:
                raise ValidationError('Correct answer must be one of the provided options')
    
    def get_options_display(self):
        """Return a formatted string of options for display"""
        if not self.options:
            return "No options"
        if self.question_type == 'true_false':
            return "True / False"
        return " | ".join(self.options)
    
    def __str__(self):
        return self.question_text[:100] + "..." if len(self.question_text) > 100 else self.question_text
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class QuestionPackage(models.Model):
    """Base question package model"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    TYPE_CHOICES = [
        ('organizational', 'Organizational'),
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)
    
    organization = models.ForeignKey(
        Organisation, 
        on_delete=models.CASCADE, 
        related_name='question_packages',
        blank=True, 
        null=True
    )
    
    created_by = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='created_packages'
    )
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('organization-only', 'Organization Only'),
        ('private', 'Private'),
    ]
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    
    # Pricing information
    pricing_type = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('paid', 'Paid'),
            ('subscription', 'Subscription'),
        ],
        default='free'
    )
    pricing_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pricing_currency = models.CharField(max_length=3, default='USD', blank=True)
    
    # Metadata
    target_audience = models.CharField(max_length=255, blank=True)
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='intermediate'
    )
    estimated_duration = models.IntegerField(help_text="Duration in minutes", default=30)
    language = models.CharField(max_length=10, default='en')
    tags = models.JSONField(default=list, blank=True)
    version = models.CharField(max_length=20, default='1.0')
    
    # Questions relationship
    questions = models.ManyToManyField(Question, related_name='packages', blank=True)
    
    # Analytics
    total_attempts = models.IntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.type})"
    
    class Meta:
        verbose_name = 'Question Package'
        verbose_name_plural = 'Question Packages'


class OrganizationalPackage(models.Model):
    """Extended model for organizational packages"""
    base_package = models.OneToOneField(
        QuestionPackage,
        on_delete=models.CASCADE,
        related_name='organizational_details'
    )
    
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Compliance information
    compliance_required = models.BooleanField(default=False)
    compliance_deadline = models.DateTimeField(blank=True, null=True)
    certification_level = models.CharField(max_length=100, blank=True, null=True)
    
    # Access control
    allowed_roles = models.JSONField(default=list, blank=True)
    allowed_departments = models.JSONField(default=list, blank=True)
    specific_users = models.ManyToManyField(Player, related_name='specific_packages', blank=True)
    
    def __str__(self):
        return f"Org Package: {self.base_package.name}"
    
    class Meta:
        verbose_name = 'Organizational Package'
        verbose_name_plural = 'Organizational Packages'


class PublicPackage(models.Model):
    """Extended model for public packages"""
    base_package = models.OneToOneField(
        QuestionPackage,
        on_delete=models.CASCADE,
        related_name='public_details'
    )
    
    # Licensing information
    LICENSING_CHOICES = [
        ('open', 'Open'),
        ('commercial', 'Commercial'),
        ('educational', 'Educational'),
    ]
    licensing_type = models.CharField(max_length=20, choices=LICENSING_CHOICES, default='open')
    attribution_required = models.BooleanField(default=False)
    
    # Reviews
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Public Package: {self.base_package.name}"
    
    class Meta:
        verbose_name = 'Public Package'
        verbose_name_plural = 'Public Packages'


class PackageAttempt(models.Model):
    """Track user attempts on question packages"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='package_attempts')
    package = models.ForeignKey(QuestionPackage, on_delete=models.CASCADE, related_name='attempts')
    
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    time_taken = models.IntegerField(help_text="Time in seconds", blank=True, null=True)
    completed = models.BooleanField(default=False)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.player.username} - {self.package.name} ({self.score}%)"
    
    class Meta:
        verbose_name = 'Package Attempt'
        verbose_name_plural = 'Package Attempts'
