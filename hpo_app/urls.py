from django.urls import path
from . import views

app_name = 'hpo_app'

urlpatterns = [
    # API endpoints for questions
    path('api/questions/', views.questions_api, name='questions_api'),
    path('api/questions/<int:question_id>/', views.question_detail_api, name='question_detail_api'),
    path('api/questions/by-card/', views.questions_by_card_api, name='questions_by_card_api'),
    path('api/packages/', views.packages_api, name='packages_api'),
    path('api/packages/<int:package_id>/questions/', views.package_questions_api, name='package_questions_api'),
    
    # Game API endpoints (unauthenticated)
    path('api/games/create/', views.create_game_api, name='create_game_api'),
    path('api/games/complete/', views.complete_game_api, name='complete_game_api'),
    path('api/games/<uuid:match_id>/responses/', views.get_game_responses_api, name='get_game_responses_api'),
    path('api/games/<uuid:match_id>/status/', views.get_game_status_api, name='get_game_status_api'),
    path('api/games/submit-answer/', views.submit_answer_api, name='submit_answer_api'),
    
    # Player statistics API endpoints
    path('api/players/<str:username>/stats/', views.get_player_stats_api, name='get_player_stats_api'),
    path('api/leaderboard/', views.get_leaderboard_api, name='get_leaderboard_api'),
]
