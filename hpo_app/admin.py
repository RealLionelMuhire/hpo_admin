from django.contrib import admin
from django import forms
from .models import (
    Organisation, Admin, Group, Player, Question, QuestionPackage, 
    OrganizationalPackage, PublicPackage, PackageAttempt
)
from .forms import QuestionAdminForm

# Customize admin site headers and titles
admin.site.site_header = "HPO Administration"
admin.site.site_title = "HPO Admin Portal"
admin.site.index_title = "Welcome to HPO Administration"


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'created_at']
    search_fields = ['name', 'contact_email', 'registration_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'role', 'organisation', 'access_level']
    list_filter = ['role', 'access_level', 'organisation', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'first_name', 'last_name', 'email')
        }),
        ('Role & Access', {
            'fields': ('role', 'access_level', 'organisation')
        }),
        ('Work Information', {
            'fields': ('department', 'employee_id', 'start_date', 'supervisor')
        }),
        ('Contact & Personal', {
            'fields': ('phone', 'bio', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'created_by', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'organization', 'subscription_type', 'points']
    list_filter = ['subscription_type', 'subscription_status', 'gender', 'education_level', 'organization']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    filter_horizontal = ['groups']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'username', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'address', 'education_level', 'interests', 'notes')
        }),
        ('Organization & Groups', {
            'fields': ('organization', 'organisation', 'group', 'groups')
        }),
        ('Subscription & Gaming', {
            'fields': ('subscription_type', 'subscription_status', 'points', 'total_attempts')
        }),
        ('Emergency Contacts', {
            'fields': ('emergency_contact', 'emergency_phone', 'parent_guardian', 'parent_phone'),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('uuid', 'password_reset_token', 'password_reset_expires', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ['question_text', 'question_type', 'get_options_display', 'get_card_display', 'correct_answer', 'difficulty', 'points', 'created_at']
    list_filter = ['question_type', 'difficulty', 'card', 'created_at']
    search_fields = ['question_text', 'correct_answer', 'card']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_options_display(self, obj):
        return obj.get_options_display()
    get_options_display.short_description = 'Options'
    
    def get_card_display(self, obj):
        return obj.get_card_display()
    get_card_display.short_description = 'Card'
    
    fieldsets = (
        ('Question', {
            'fields': ('question_text', 'question_type'),
            'description': 'Enter your question and select the type'
        }),
        ('Answer Options - Multiple Choice', {
            'fields': ('option_1', 'option_2', 'option_3', 'option_4'),
            'description': 'For Multiple Choice: Enter 2-4 options (at least 2 required)',
            'classes': ('multiple-choice-options',)
        }),
        ('Correct Answer & Explanation', {
            'fields': ('correct_answer', 'explanation'),
            'description': 'For True/False: Select "True" or "False". For Multiple Choice: Type the exact text of the correct option'
        }),
        ('Scoring & Difficulty', {
            'fields': ('points', 'difficulty')
        }),
        ('Card Association', {
            'fields': ('card',),
            'description': 'Associate this question with a playing card (optional)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form based on question type"""
        form = super().get_form(request, obj, **kwargs)
        return form


@admin.register(QuestionPackage)
class QuestionPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'category', 'status', 'created_by', 'total_attempts', 'created_at']
    list_filter = ['type', 'status', 'visibility', 'pricing_type', 'difficulty', 'created_at']
    search_fields = ['name', 'description', 'category']
    readonly_fields = ['total_attempts', 'average_score', 'completion_rate', 'created_at', 'updated_at']
    filter_horizontal = ['questions']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'type', 'category', 'visibility', 'status')
        }),
        ('Organization & Creator', {
            'fields': ('organization', 'created_by')
        }),
        ('Pricing', {
            'fields': ('pricing_type', 'pricing_amount', 'pricing_currency')
        }),
        ('Metadata', {
            'fields': ('target_audience', 'difficulty', 'estimated_duration', 'language', 'tags', 'version')
        }),
        ('Questions', {
            'fields': ('questions',)
        }),
        ('Analytics', {
            'fields': ('total_attempts', 'average_score', 'completion_rate'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class OrganizationalPackageInline(admin.StackedInline):
    model = OrganizationalPackage
    extra = 0


class PublicPackageInline(admin.StackedInline):
    model = PublicPackage
    extra = 0


@admin.register(OrganizationalPackage)
class OrganizationalPackageAdmin(admin.ModelAdmin):
    list_display = ['base_package', 'department', 'compliance_required', 'compliance_deadline']
    list_filter = ['compliance_required', 'department']
    search_fields = ['base_package__name', 'department']
    filter_horizontal = ['specific_users']
    
    fieldsets = (
        ('Package Reference', {
            'fields': ('base_package',)
        }),
        ('Organizational Details', {
            'fields': ('department',)
        }),
        ('Compliance', {
            'fields': ('compliance_required', 'compliance_deadline', 'certification_level')
        }),
        ('Access Control', {
            'fields': ('allowed_roles', 'allowed_departments', 'specific_users')
        })
    )


@admin.register(PublicPackage)
class PublicPackageAdmin(admin.ModelAdmin):
    list_display = ['base_package', 'licensing_type', 'rating', 'total_reviews', 'attribution_required']
    list_filter = ['licensing_type', 'attribution_required']
    search_fields = ['base_package__name']
    
    fieldsets = (
        ('Package Reference', {
            'fields': ('base_package',)
        }),
        ('Licensing', {
            'fields': ('licensing_type', 'attribution_required')
        }),
        ('Reviews', {
            'fields': ('rating', 'total_reviews')
        })
    )


@admin.register(PackageAttempt)
class PackageAttemptAdmin(admin.ModelAdmin):
    list_display = ['player', 'package', 'score', 'completed', 'started_at', 'completed_at']
    list_filter = ['completed', 'package__type', 'started_at']
    search_fields = ['player__username', 'player__first_name', 'player__last_name', 'package__name']
    readonly_fields = ['started_at']
    
    fieldsets = (
        ('Attempt Details', {
            'fields': ('player', 'package', 'completed')
        }),
        ('Scoring', {
            'fields': ('score', 'total_questions', 'correct_answers', 'time_taken')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at')
        })
    )
