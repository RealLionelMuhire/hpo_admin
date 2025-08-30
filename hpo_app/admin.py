from django.contrib import admin
from django import forms
from django.db import models
from .models import (
    Organisation, Admin, Group, Player, Question, QuestionPackage, 
    OrganizationalPackage, PublicPackage, PackageAttempt,
    Game, GameParticipant, GameResult, GameResponse, 
    Topic, Subtopic, GameContent
)
from .forms import QuestionAdminForm, PlayerAdminForm, GameContentAdminForm

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
    
    # Custom Actions
    actions = ['activate_payment', 'deactivate_payment', 'set_pending_payment']
    
    def activate_payment(self, request, queryset):
        updated = queryset.update(payment_status='active')
        self.message_user(request, f'{updated} organizations were activated.')
    activate_payment.short_description = "Activate payment for selected organizations"
    
    def deactivate_payment(self, request, queryset):
        updated = queryset.update(payment_status='inactive')
        self.message_user(request, f'{updated} organizations were deactivated.')
    deactivate_payment.short_description = "Deactivate payment for selected organizations"
    
    def set_pending_payment(self, request, queryset):
        updated = queryset.update(payment_status='pending')
        self.message_user(request, f'{updated} organizations set to pending payment.')
    set_pending_payment.short_description = "Set payment status to pending for selected organizations"


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'role', 'organisation', 'access_level']
    list_filter = ['role', 'access_level', 'organisation', 'created_at']
    search_fields = ['name', 'first_name', 'last_name', 'email', 'employee_id']
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
    list_display = ['name', 'level', 'created_by', 'created_at'
]
    list_filter = ['level', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm
    list_display = [
        'player_name', 'username', 'phone', 'age_group', 'province', 
        'organization', 'subscription_type', 'points', 'games_played', 
        'games_won', 'win_rate_display', 'total_game_marks'
    ]
    list_filter = [
        'subscription_type', 'subscription_status', 'age_group', 'gender', 
        'province', 'district', 'education_level', 'organization', 
        'last_game_result'
    ]
    search_fields = ['player_name', 'username', 'email', 'phone']
    readonly_fields = [
        'uuid', 'created_at', 'updated_at', 'win_rate', 'answer_accuracy', 
        'average_marks_per_game', 'last_game_played'
    ]
    filter_horizontal = ['groups']
    
    def win_rate_display(self, obj):
        return f"{obj.win_rate}%"
    win_rate_display.short_description = "Win Rate"
    
    # Custom Actions
    actions = [
        'make_premium', 'make_free', 'reset_points', 'reset_game_stats',
        'update_to_kigali', 'bulk_edit_age_group'
    ]
    
    def reset_game_stats(self, request, queryset):
        updated = queryset.update(
            games_played=0, games_won=0, games_lost=0, total_game_marks=0,
            questions_answered=0, correct_answers=0, current_win_streak=0,
            longest_win_streak=0, last_game_played=None, last_game_result=None
        )
        self.message_user(request, f'Game statistics reset for {updated} players.')
    reset_game_stats.short_description = "Reset game statistics for selected players"
    
    def make_premium(self, request, queryset):
        updated = queryset.update(subscription_type='premium')
        self.message_user(request, f'{updated} players were successfully marked as premium.')
    make_premium.short_description = "Mark selected players as Premium"
    
    def make_free(self, request, queryset):
        updated = queryset.update(subscription_type='free')
        self.message_user(request, f'{updated} players were successfully marked as free.')
    make_free.short_description = "Mark selected players as Free"
    
    def reset_points(self, request, queryset):
        updated = queryset.update(points=0, total_attempts=0)
        self.message_user(request, f'Points and attempts reset for {updated} players.')
    reset_points.short_description = "Reset points and attempts for selected players"
    
    def update_to_kigali(self, request, queryset):
        updated = queryset.update(province='Kigali City', district='Gasabo')
        self.message_user(request, f'{updated} players moved to Kigali City, Gasabo district.')
    update_to_kigali.short_description = "Move selected players to Kigali City (Gasabo)"
    
    def bulk_edit_age_group(self, request, queryset):
        # This could be enhanced with a custom form
        updated = queryset.update(age_group='20-24')
        self.message_user(request, f'{updated} players age group updated to 20-24.')
    bulk_edit_age_group.short_description = "Set age group to 20-24 for selected players"
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('player_name', 'username', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('age_group', 'gender', 'education_level')
        }),
        ('Location (Rwanda)', {
            'fields': ('province', 'district'),
            'description': 'Select your location in Rwanda'
        }),
        ('Organization & Groups', {
            'fields': ('organization', 'group', 'groups')
        }),
        ('Subscription & Gaming', {
            'fields': ('subscription_type', 'subscription_status', 'points', 'total_attempts')
        }),
        ('Game Statistics', {
            'fields': (
                'games_played', 'games_won', 'games_lost', 'total_game_marks',
                'win_rate', 'average_marks_per_game'
            ),
            'description': 'Game performance metrics'
        }),
        ('Question Statistics', {
            'fields': (
                'questions_answered', 'correct_answers', 'answer_accuracy'
            ),
            'description': 'Question answering performance'
        }),
        ('Achievements & Streaks', {
            'fields': (
                'current_win_streak', 'longest_win_streak', 
                'last_game_played', 'last_game_result'
            ),
            'classes': ('collapse',)
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
    
    # Custom Actions
    actions = ['make_easy', 'make_medium', 'make_hard', 'add_points', 'remove_card_association', 'assign_to_spades']
    
    def make_easy(self, request, queryset):
        updated = queryset.update(difficulty='easy')
        self.message_user(request, f'{updated} questions were marked as Easy.')
    make_easy.short_description = "Mark selected questions as Easy"
    
    def make_medium(self, request, queryset):
        updated = queryset.update(difficulty='medium')
        self.message_user(request, f'{updated} questions were marked as Medium.')
    make_medium.short_description = "Mark selected questions as Medium"
    
    def make_hard(self, request, queryset):
        updated = queryset.update(difficulty='hard')
        self.message_user(request, f'{updated} questions were marked as Hard.')
    make_hard.short_description = "Mark selected questions as Hard"
    
    def add_points(self, request, queryset):
        updated = queryset.update(points=models.F('points') + 1)
        self.message_user(request, f'Added 1 point to {updated} questions.')
    add_points.short_description = "Add 1 point to selected questions"
    
    def remove_card_association(self, request, queryset):
        updated = queryset.update(card=None)
        self.message_user(request, f'Removed card association from {updated} questions.')
    remove_card_association.short_description = "Remove card association from selected questions"
    
    def assign_to_spades(self, request, queryset):
        updated = queryset.update(card='S7')  # Assign to Spades 7 (10 points)
        self.message_user(request, f'Assigned {updated} questions to Spades 7 card.')
    assign_to_spades.short_description = "Assign selected questions to Spades 7 card"
    
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
    search_fields = ['player__username', 'player__player_name', 'package__name']
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


# ==================== GAME ADMIN CONFIGURATIONS ====================

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'match_id_short', 'participant_count', 'team_count', 'status', 
        'winning_team', 'created_at', 'completed_at'
    ]
    list_filter = ['status', 'participant_count', 'winning_team', 'created_at']
    search_fields = ['match_id']
    readonly_fields = ['match_id', 'team_count', 'created_at', 'completed_at']
    
    fieldsets = (
        ('Game Information', {
            'fields': ('match_id', 'participant_count', 'team_count', 'status')
        }),
        ('Game Results', {
            'fields': ('winning_team', 'cards_chosen')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        })
    )
    
    def match_id_short(self, obj):
        return str(obj.match_id)[:8] + "..."
    match_id_short.short_description = "Match ID"
    
    actions = ['mark_completed', 'mark_cancelled']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} games marked as completed.')
    mark_completed.short_description = "Mark selected games as completed"
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} games marked as cancelled.')
    mark_cancelled.short_description = "Mark selected games as cancelled"


@admin.register(GameParticipant)
class GameParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'player', 'game_match_id', 'team', 'is_winner', 'marks_earned', 
        'lost_card', 'question_answered', 'answer_correct'
    ]
    list_filter = [
        'team', 'is_winner', 'question_answered', 'answer_correct', 
        'game__status', 'joined_at'
    ]
    search_fields = ['player__username', 'player__player_name', 'game__match_id']
    readonly_fields = ['joined_at']
    
    fieldsets = (
        ('Game Participation', {
            'fields': ('game', 'player', 'team', 'joined_at')
        }),
        ('Game Results', {
            'fields': ('is_winner', 'marks_earned', 'lost_card')
        }),
        ('Question Response', {
            'fields': ('question_answered', 'answer_correct')
        })
    )
    
    def game_match_id(self, obj):
        return str(obj.game.match_id)[:8] + "..."
    game_match_id.short_description = "Game Match ID"
    
    actions = ['mark_as_winner', 'mark_as_loser']
    
    def mark_as_winner(self, request, queryset):
        updated = queryset.update(is_winner=True, marks_earned=1)
        self.message_user(request, f'{updated} participants marked as winners.')
    mark_as_winner.short_description = "Mark selected participants as winners"
    
    def mark_as_loser(self, request, queryset):
        updated = queryset.update(is_winner=False, marks_earned=0)
        self.message_user(request, f'{updated} participants marked as losers.')
    mark_as_loser.short_description = "Mark selected participants as losers"


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = [
        'game_match_id', 'team1_marks', 'team2_marks', 'total_marks', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['game__match_id']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Game Information', {
            'fields': ('game',)
        }),
        ('Team Scores', {
            'fields': ('team1_marks', 'team2_marks')
        }),
        ('Game Summary', {
            'fields': ('result_summary',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )
    
    def game_match_id(self, obj):
        return str(obj.game.match_id)[:8] + "..."
    game_match_id.short_description = "Game Match ID"
    
    def total_marks(self, obj):
        return obj.team1_marks + obj.team2_marks
    total_marks.short_description = "Total Marks"


@admin.register(GameResponse)
class GameResponseAdmin(admin.ModelAdmin):
    list_display = [
        'participant_player', 'game_match_id', 'response_type', 
        'is_correct', 'created_at'
    ]
    list_filter = [
        'response_type', 'is_correct', 'created_at',
        'game__status'
    ]
    search_fields = [
        'participant__player__username', 'participant__player__player_name',
        'game__match_id', 'question__question_text'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Response Information', {
            'fields': ('game', 'participant', 'response_type', 'created_at')
        }),
        ('Fun Fact (Winners)', {
            'fields': ('fun_fact_text', 'fun_fact_card'),
            'classes': ('collapse',)
        }),
        ('Question Response (Losers)', {
            'fields': ('question', 'player_answer', 'is_correct'),
            'classes': ('collapse',)
        })
    )
    
    def participant_player(self, obj):
        return obj.participant.player.username
    participant_player.short_description = "Player"
    
    def game_match_id(self, obj):
        return str(obj.game.match_id)[:8] + "..."
    game_match_id.short_description = "Game Match ID"
    
    actions = ['mark_correct', 'mark_incorrect']
    
    def mark_correct(self, request, queryset):
        updated = queryset.filter(response_type='question').update(is_correct=True)
        self.message_user(request, f'{updated} question responses marked as correct.')
    mark_correct.short_description = "Mark selected question responses as correct"
    
    def mark_incorrect(self, request, queryset):
        updated = queryset.filter(response_type='question').update(is_correct=False)
        self.message_user(request, f'{updated} question responses marked as incorrect.')
    mark_incorrect.short_description = "Mark selected question responses as incorrect"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'get_subtopics_count', 'get_content_count', 'is_active', 'created_at']
    list_filter = ['language', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'get_subtopics_count', 'get_content_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'language', 'description', 'is_active')
        }),
        ('Statistics', {
            'fields': ('get_subtopics_count', 'get_content_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_subtopics_count(self, obj):
        return obj.get_subtopics_count()
    get_subtopics_count.short_description = "Subtopics Count"
    
    def get_content_count(self, obj):
        return obj.get_content_count()
    get_content_count.short_description = "Total Content Count"


class SubtopicInline(admin.TabularInline):
    model = Subtopic
    extra = 1
    fields = ['name', 'description', 'order', 'is_active']
    ordering = ['order', 'name']


@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'get_topic_language', 'get_content_count', 'order', 'is_active', 'created_at']
    list_filter = ['topic__language', 'topic', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'topic__name']
    readonly_fields = ['created_at', 'updated_at', 'get_content_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'name', 'description', 'order', 'is_active')
        }),
        ('Statistics', {
            'fields': ('get_content_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_topic_language(self, obj):
        return obj.topic.language
    get_topic_language.short_description = "Language"
    
    def get_content_count(self, obj):
        return obj.get_content_count()
    get_content_count.short_description = "Content Count"


# Add inline to Topic admin
TopicAdmin.inlines = [SubtopicInline]


@admin.register(GameContent)
class GameContentAdmin(admin.ModelAdmin):
    form = GameContentAdminForm
    
    list_display = [
        'topic', 
        'subtopic', 
        'language', 
        'age_group', 
        'content_type',
        'get_subtopics_count',
        'status', 
        'view_count', 
        'usage_count',
        'created_at'
    ]
    
    list_filter = [
        'language',
        'age_group', 
        'content_type',
        'difficulty_level',
        'status',
        'created_at'
    ]
    
    search_fields = [
        'topic',
        'subtopic', 
        'info',
        'title',
        'tags'
    ]
    
    readonly_fields = [
        'view_count', 
        'usage_count', 
        'created_at', 
        'updated_at',
        'get_all_subtopics_display'
    ]
    
    fieldsets = (
        ('Basic Information (Required)', {
            'fields': (
                'language',
                'age_group', 
                'topic',
                'subtopic',
                'info'
            ),
            'description': 'Fill in these required fields manually like in a handbook'
        }),
        ('Multiple Subtopics', {
            'fields': (
                'get_all_subtopics_display',
                'additional_subtopics',
            ),
            'description': 'Add multiple subtopics with their own information. The main subtopic is shown above.',
        }),
        ('Additional Details', {
            'fields': (
                'title',
                'content_type',
                'difficulty_level',
                'status',
                'tags'
            ),
            'classes': ('collapse',)
        }),
        ('Associations', {
            'fields': (
                'related_question',
                'card_association'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'created_by',
                'approved_by',
                'view_count',
                'usage_count',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def get_subtopics_count(self, obj):
        """Display the total number of subtopics"""
        return obj.get_subtopics_count()
    get_subtopics_count.short_description = 'Subtopics Count'
    
    def get_all_subtopics_display(self, obj):
        """Display all subtopics for read-only view"""
        from django.utils.safestring import mark_safe
        
        if not obj.pk:
            return "Save the content first to add multiple subtopics"
        
        subtopics = obj.get_all_subtopics()
        if not subtopics:
            return "No subtopics added"
        
        html = "<div style='max-width: 600px;'>"
        for i, subtopic_data in enumerate(subtopics):
            primary_label = " (Primary)" if subtopic_data.get('is_primary') else ""
            html += f"<div style='margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'>"
            html += f"<strong>{i+1}. {subtopic_data['subtopic']}{primary_label}</strong><br>"
            html += f"<em>{subtopic_data['info'][:200]}{'...' if len(subtopic_data['info']) > 200 else ''}</em>"
            html += "</div>"
        html += "</div>"
        return mark_safe(html)
    get_all_subtopics_display.short_description = 'All Subtopics'
    
    class Media:
        css = {
            'all': ('admin/css/gamecontent_admin.css',)
        }
        js = ('admin/js/gamecontent_admin.js',)
    
    ordering = ['-created_at']
    
    actions = ['mark_as_published', 'mark_as_draft', 'mark_as_archived']
    
    def mark_as_published(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f"{queryset.count()} content items marked as published.")
    mark_as_published.short_description = "Mark selected content as Published"
    
    def mark_as_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f"{queryset.count()} content items marked as draft.")
    mark_as_draft.short_description = "Mark selected content as Draft"
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
        self.message_user(request, f"{queryset.count()} content items archived.")
    mark_as_archived.short_description = "Archive selected content"
