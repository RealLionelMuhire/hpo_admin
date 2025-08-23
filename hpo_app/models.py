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
    player_name = models.CharField(max_length=200, help_text="Full name of the player", default="Unknown Player")
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6)])
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    AGE_GROUP_CHOICES = [
        ('10-15', '10-15'),
        ('16-21', '16-21'),
        ('21-29', '21-29'),
        ('above', 'Above 29'),
    ]
    age_group = models.CharField(
        max_length=10, 
        choices=AGE_GROUP_CHOICES, 
        blank=True, 
        null=True,
        help_text="Select age group"
    )
    
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
    
    # Rwanda Location Fields
    PROVINCE_CHOICES = [
        ('Kigali City', 'Kigali City'),
        ('Northern Province', 'Northern Province'),
        ('Southern Province', 'Southern Province'),
        ('Eastern Province', 'Eastern Province'),
        ('Western Province', 'Western Province'),
    ]
    province = models.CharField(
        max_length=30,
        choices=PROVINCE_CHOICES,
        blank=True,
        null=True,
        help_text="Select province in Rwanda"
    )
    
    DISTRICT_CHOICES = [
        # Kigali City
        ('Gasabo', 'Gasabo'),
        ('Kicukiro', 'Kicukiro'),
        ('Nyarugenge', 'Nyarugenge'),
        # Northern Province
        ('Burera', 'Burera'),
        ('Gakenke', 'Gakenke'),
        ('Gicumbi', 'Gicumbi'),
        ('Musanze', 'Musanze'),
        ('Rulindo', 'Rulindo'),
        # Southern Province
        ('Gisagara', 'Gisagara'),
        ('Huye', 'Huye'),
        ('Kamonyi', 'Kamonyi'),
        ('Muhanga', 'Muhanga'),
        ('Nyamagabe', 'Nyamagabe'),
        ('Nyanza', 'Nyanza'),
        ('Nyaruguru', 'Nyaruguru'),
        ('Ruhango', 'Ruhango'),
        # Eastern Province
        ('Bugesera', 'Bugesera'),
        ('Gatsibo', 'Gatsibo'),
        ('Kayonza', 'Kayonza'),
        ('Kirehe', 'Kirehe'),
        ('Ngoma', 'Ngoma'),
        ('Nyagatare', 'Nyagatare'),
        ('Rwamagana', 'Rwamagana'),
        # Western Province
        ('Karongi', 'Karongi'),
        ('Ngororero', 'Ngororero'),
        ('Nyabihu', 'Nyabihu'),
        ('Nyamasheke', 'Nyamasheke'),
        ('Rubavu', 'Rubavu'),
        ('Rusizi', 'Rusizi'),
        ('Rutsiro', 'Rutsiro'),
    ]
    district = models.CharField(
        max_length=30,
        choices=DISTRICT_CHOICES,
        blank=True,
        null=True,
        help_text="Select district in Rwanda"
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
    
    # Game-related statistics
    games_played = models.IntegerField(default=0, help_text="Total number of games played")
    games_won = models.IntegerField(default=0, help_text="Total number of games won")
    games_lost = models.IntegerField(default=0, help_text="Total number of games lost")
    total_game_marks = models.IntegerField(default=0, help_text="Total marks earned from games")
    questions_answered = models.IntegerField(default=0, help_text="Total questions answered in games")
    correct_answers = models.IntegerField(default=0, help_text="Total correct answers in games")
    
    # Game streaks and achievements
    current_win_streak = models.IntegerField(default=0, help_text="Current consecutive wins")
    longest_win_streak = models.IntegerField(default=0, help_text="Longest win streak achieved")
    
    # Last game activity
    last_game_played = models.DateTimeField(blank=True, null=True, help_text="Last time player participated in a game")
    last_game_result = models.CharField(
        max_length=10,
        choices=[
            ('won', 'Won'),
            ('lost', 'Lost'),
        ],
        blank=True,
        null=True,
        help_text="Result of the last game played"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def win_rate(self):
        """Calculate win rate percentage"""
        if self.games_played == 0:
            return 0.0
        return round((self.games_won / self.games_played) * 100, 2)
    
    @property
    def answer_accuracy(self):
        """Calculate answer accuracy percentage"""
        if self.questions_answered == 0:
            return 0.0
        return round((self.correct_answers / self.questions_answered) * 100, 2)
    
    @property
    def average_marks_per_game(self):
        """Calculate average marks earned per game"""
        if self.games_played == 0:
            return 0.0
        return round(self.total_game_marks / self.games_played, 2)
    
    def update_game_stats(self, won=False, marks_earned=0, questions_answered=0, correct_answers=0):
        """Update player's game statistics after a game"""
        from django.utils import timezone
        
        self.games_played += 1
        if won:
            self.games_won += 1
            self.current_win_streak += 1
            if self.current_win_streak > self.longest_win_streak:
                self.longest_win_streak = self.current_win_streak
            self.last_game_result = 'won'
        else:
            self.games_lost += 1
            self.current_win_streak = 0
            self.last_game_result = 'lost'
        
        self.total_game_marks += marks_earned
        self.questions_answered += questions_answered
        self.correct_answers += correct_answers
        self.last_game_played = timezone.now()
        self.save()
    
    def get_game_history_summary(self):
        """Get a summary of player's game history"""
        return {
            'total_games': self.games_played,
            'wins': self.games_won,
            'losses': self.games_lost,
            'win_rate': self.win_rate,
            'total_marks': self.total_game_marks,
            'average_marks_per_game': self.average_marks_per_game,
            'current_streak': self.current_win_streak,
            'longest_streak': self.longest_win_streak,
            'answer_accuracy': self.answer_accuracy,
            'last_played': self.last_game_played,
            'last_result': self.last_game_result
        }
    
    def __str__(self):
        return f"{self.player_name} ({self.username})"
    
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
    
    # Card association
    CARD_CHOICES = [
        # Spades
        ('S3', 'Spades 3'),
        ('S4', 'Spades 4'),
        ('S5', 'Spades 5'),
        ('S6', 'Spades 6'),
        ('S7', 'Spades 7'),
        ('SJ', 'Spades Jack'),
        ('SQ', 'Spades Queen'),
        ('SK', 'Spades King'),
        ('SA', 'Spades Ace'),
        # Hearts
        ('H3', 'Hearts 3'),
        ('H4', 'Hearts 4'),
        ('H5', 'Hearts 5'),
        ('H6', 'Hearts 6'),
        ('H7', 'Hearts 7'),
        ('HJ', 'Hearts Jack'),
        ('HQ', 'Hearts Queen'),
        ('HK', 'Hearts King'),
        ('HA', 'Hearts Ace'),
        # Clubs
        ('C3', 'Clubs 3'),
        ('C4', 'Clubs 4'),
        ('C5', 'Clubs 5'),
        ('C6', 'Clubs 6'),
        ('C7', 'Clubs 7'),
        ('CJ', 'Clubs Jack'),
        ('CQ', 'Clubs Queen'),
        ('CK', 'Clubs King'),
        ('CA', 'Clubs Ace'),
        # Diamonds
        ('D3', 'Diamonds 3'),
        ('D4', 'Diamonds 4'),
        ('D5', 'Diamonds 5'),
        ('D6', 'Diamonds 6'),
        ('D7', 'Diamonds 7'),
        ('DJ', 'Diamonds Jack'),
        ('DQ', 'Diamonds Queen'),
        ('DK', 'Diamonds King'),
        ('DA', 'Diamonds Ace'),
    ]
    
    card = models.CharField(
        max_length=3,
        choices=CARD_CHOICES,
        blank=True,
        null=True,
        help_text="Associate this question with a playing card"
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
    
    # Track who created this question
    created_by = models.ForeignKey(
        Admin,
        on_delete=models.CASCADE,
        related_name='created_questions',
        blank=True,
        null=True,
        help_text="Admin who created this question"
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
    
    def get_card_info(self):
        """Return card information as a dictionary"""
        if not self.card:
            return None
        
        # Card data mapping
        card_data = {
            # Spades
            'S3': {'suit': 'Spades', 'value': '3', 'pointValue': 0, 'symbol': '♠'},
            'S4': {'suit': 'Spades', 'value': '4', 'pointValue': 0, 'symbol': '♠'},
            'S5': {'suit': 'Spades', 'value': '5', 'pointValue': 0, 'symbol': '♠'},
            'S6': {'suit': 'Spades', 'value': '6', 'pointValue': 0, 'symbol': '♠'},
            'S7': {'suit': 'Spades', 'value': '7', 'pointValue': 10, 'symbol': '♠'},
            'SJ': {'suit': 'Spades', 'value': 'J', 'pointValue': 3, 'symbol': '♠'},
            'SQ': {'suit': 'Spades', 'value': 'Q', 'pointValue': 2, 'symbol': '♠'},
            'SK': {'suit': 'Spades', 'value': 'K', 'pointValue': 4, 'symbol': '♠'},
            'SA': {'suit': 'Spades', 'value': 'A', 'pointValue': 11, 'symbol': '♠'},
            # Hearts
            'H3': {'suit': 'Hearts', 'value': '3', 'pointValue': 0, 'symbol': '♥'},
            'H4': {'suit': 'Hearts', 'value': '4', 'pointValue': 0, 'symbol': '♥'},
            'H5': {'suit': 'Hearts', 'value': '5', 'pointValue': 0, 'symbol': '♥'},
            'H6': {'suit': 'Hearts', 'value': '6', 'pointValue': 0, 'symbol': '♥'},
            'H7': {'suit': 'Hearts', 'value': '7', 'pointValue': 10, 'symbol': '♥'},
            'HJ': {'suit': 'Hearts', 'value': 'J', 'pointValue': 3, 'symbol': '♥'},
            'HQ': {'suit': 'Hearts', 'value': 'Q', 'pointValue': 2, 'symbol': '♥'},
            'HK': {'suit': 'Hearts', 'value': 'K', 'pointValue': 4, 'symbol': '♥'},
            'HA': {'suit': 'Hearts', 'value': 'A', 'pointValue': 11, 'symbol': '♥'},
            # Clubs
            'C3': {'suit': 'Clubs', 'value': '3', 'pointValue': 0, 'symbol': '♣'},
            'C4': {'suit': 'Clubs', 'value': '4', 'pointValue': 0, 'symbol': '♣'},
            'C5': {'suit': 'Clubs', 'value': '5', 'pointValue': 0, 'symbol': '♣'},
            'C6': {'suit': 'Clubs', 'value': '6', 'pointValue': 0, 'symbol': '♣'},
            'C7': {'suit': 'Clubs', 'value': '7', 'pointValue': 10, 'symbol': '♣'},
            'CJ': {'suit': 'Clubs', 'value': 'J', 'pointValue': 3, 'symbol': '♣'},
            'CQ': {'suit': 'Clubs', 'value': 'Q', 'pointValue': 2, 'symbol': '♣'},
            'CK': {'suit': 'Clubs', 'value': 'K', 'pointValue': 4, 'symbol': '♣'},
            'CA': {'suit': 'Clubs', 'value': 'A', 'pointValue': 11, 'symbol': '♣'},
            # Diamonds
            'D3': {'suit': 'Diamonds', 'value': '3', 'pointValue': 0, 'symbol': '♦'},
            'D4': {'suit': 'Diamonds', 'value': '4', 'pointValue': 0, 'symbol': '♦'},
            'D5': {'suit': 'Diamonds', 'value': '5', 'pointValue': 0, 'symbol': '♦'},
            'D6': {'suit': 'Diamonds', 'value': '6', 'pointValue': 0, 'symbol': '♦'},
            'D7': {'suit': 'Diamonds', 'value': '7', 'pointValue': 10, 'symbol': '♦'},
            'DJ': {'suit': 'Diamonds', 'value': 'J', 'pointValue': 3, 'symbol': '♦'},
            'DQ': {'suit': 'Diamonds', 'value': 'Q', 'pointValue': 2, 'symbol': '♦'},
            'DK': {'suit': 'Diamonds', 'value': 'K', 'pointValue': 4, 'symbol': '♦'},
            'DA': {'suit': 'Diamonds', 'value': 'A', 'pointValue': 11, 'symbol': '♦'},
        }
        
        card_info = card_data.get(self.card, {})
        card_info['id'] = self.card
        return card_info
    
    def get_card_display(self):
        """Return a formatted string for card display"""
        card_info = self.get_card_info()
        if not card_info:
            return "No card"
        return f"{card_info['symbol']} {card_info['value']} ({card_info['suit']})"
    
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


class Game(models.Model):
    """Game session model to track card game matches"""
    match_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    PARTICIPANT_CHOICES = [
        (1, '1 Player (vs Computer)'),
        (2, '2 Players'),
        (4, '4 Players'),
        (6, '6 Players'),
    ]
    participant_count = models.IntegerField(
        choices=PARTICIPANT_CHOICES,
        help_text="Number of participants in the game"
    )
    
    # Team count is calculated based on participants
    # 1 participant = 1 team (player vs computer)
    # 2+ participants = 2 teams
    team_count = models.IntegerField(default=2)
    
    # Game status
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Players'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    
    # Winning team (1 or 2, null if game not finished)
    winning_team = models.IntegerField(blank=True, null=True, choices=[(1, 'Team 1'), (2, 'Team 2')])
    
    # Cards used in this game (for tracking which questions might be needed)
    cards_in_play = models.JSONField(default=list, blank=True, help_text="List of card IDs used in this game")
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        """Auto-calculate team count based on participants"""
        if self.participant_count == 1:
            self.team_count = 1
        else:
            self.team_count = 2
        super().save(*args, **kwargs)
    
    @property
    def players_per_team(self):
        """Calculate players per team"""
        if self.participant_count == 1:
            return 1
        return self.participant_count // 2
    
    def __str__(self):
        return f"Game {str(self.match_id)[:8]} - {self.participant_count} players"
    
    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'


class GameParticipant(models.Model):
    """Players participating in a specific game"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='participants')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='game_participations')
    
    TEAM_CHOICES = [
        (1, 'Team 1'),
        (2, 'Team 2'),
    ]
    team = models.IntegerField(choices=TEAM_CHOICES, help_text="Which team the player belongs to")
    
    # Game results for this player
    is_winner = models.BooleanField(default=False)
    marks_earned = models.IntegerField(default=0, help_text="Marks earned (1 per win)")
    
    # If player lost, they get a card and must answer question
    lost_card = models.CharField(
        max_length=3,
        choices=Question.CARD_CHOICES,
        blank=True,
        null=True,
        help_text="Card assigned to losing player"
    )
    
    # Question response tracking
    question_answered = models.BooleanField(default=False)
    answer_correct = models.BooleanField(default=False)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.username} in Game {str(self.game.match_id)[:8]} (Team {self.team})"
    
    class Meta:
        verbose_name = 'Game Participant'
        verbose_name_plural = 'Game Participants'
        unique_together = ['game', 'player']


class GameResult(models.Model):
    """Store game results and responses"""
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='result')
    
    # Team marks (team 1 and team 2 marks)
    team1_marks = models.IntegerField(default=0)
    team2_marks = models.IntegerField(default=0)
    
    # Game outcome summary
    result_summary = models.JSONField(
        default=dict,
        help_text="Summary of game results, questions asked, answers given"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result for Game {str(self.game.match_id)[:8]}"
    
    class Meta:
        verbose_name = 'Game Result'
        verbose_name_plural = 'Game Results'


class GameResponse(models.Model):
    """Store player responses during game"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='responses')
    participant = models.ForeignKey(GameParticipant, on_delete=models.CASCADE, related_name='responses')
    
    RESPONSE_TYPE_CHOICES = [
        ('fun_fact', 'Fun Fact (Winner)'),
        ('question', 'Question (Loser)'),
    ]
    response_type = models.CharField(max_length=20, choices=RESPONSE_TYPE_CHOICES)
    
    # For winners: fun fact from explanation
    fun_fact_text = models.TextField(blank=True, null=True)
    fun_fact_card = models.CharField(max_length=3, blank=True, null=True)
    
    # For losers: question to answer
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='game_responses'
    )
    player_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.response_type} for {self.participant.player.username} in Game {str(self.game.match_id)[:8]}"
    
    class Meta:
        verbose_name = 'Game Response'
        verbose_name_plural = 'Game Responses'
