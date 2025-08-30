from django.urls import path, include
from .api_views import (
    PlayerRegistrationView,
    player_login_view,
    player_logout_view,
    player_profile_view,
    get_age_groups_view,
    get_provinces_districts_view,
    get_gender_choices_view
)

app_name = 'api'

urlpatterns = [
    # Player Authentication APIs
    path('auth/register/', PlayerRegistrationView.as_view(), name='player_register'),
    path('auth/login/', player_login_view, name='player_login'),
    path('auth/logout/', player_logout_view, name='player_logout'),
    path('auth/profile/', player_profile_view, name='player_profile'),
    
    # Helper APIs for form data
    path('form-data/age-groups/', get_age_groups_view, name='age_groups'),
    path('form-data/provinces-districts/', get_provinces_districts_view, name='provinces_districts'),
    path('form-data/genders/', get_gender_choices_view, name='gender_choices'),
]
