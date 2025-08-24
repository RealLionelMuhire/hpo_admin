from django.urls import path
from . import views

app_name = 'hpo_app'

urlpatterns = [
    # API endpoints for questions
    path('api/questions/', views.questions_api, name='questions_api'),
    path('api/questions/<int:question_id>/', views.question_detail_api, name='question_detail_api'),
    path('api/questions/by-card/', views.questions_by_card_api, name='questions_by_card_api'),
    path('api/cards/<str:card_id>/questions/', views.get_card_questions_api, name='get_card_questions_api'),
    path('api/packages/', views.packages_api, name='packages_api'),
    path('api/packages/<int:package_id>/questions/', views.package_questions_api, name='package_questions_api'),
    
    # Game API endpoints (unauthenticated)
    path('api/games/create/', views.create_game_api, name='create_game_api'),
    path('api/games/complete/', views.complete_game_api, name='complete_game_api'),
    path('api/games/submit-completed/', views.submit_completed_game_api, name='submit_completed_game_api'),
    path('api/games/<uuid:match_id>/responses/', views.get_game_responses_api, name='get_game_responses_api'),
    path('api/games/<uuid:match_id>/status/', views.get_game_status_api, name='get_game_status_api'),
    path('api/games/submit-answer/', views.submit_answer_api, name='submit_answer_api'),
    path('api/games/award-points/', views.award_points_api, name='award_points_api'),
    path('api/games/record-wrong-answer/', views.record_wrong_answer_api, name='record_wrong_answer_api'),
    
    # Player statistics API endpoints
    path('api/players/<str:username>/stats/', views.get_player_stats_api, name='get_player_stats_api'),
    path('api/leaderboard/', views.get_leaderboard_api, name='get_leaderboard_api'),
    
    # Game Content API endpoints
    path('api/game-content/', views.get_game_content_api, name='get_game_content_api'),
    path('api/game-content/<int:content_id>/', views.get_game_content_detail_api, name='get_game_content_detail_api'),
    path('api/game-content/<str:language>/<str:age_group>/', views.get_game_content_by_language_age_api, name='get_game_content_by_language_age_api'),
    path('api/game-content/<int:content_id>/update/', views.update_game_content_api, name='update_game_content_api'),
    path('api/game-content/<int:content_id>/delete/', views.delete_game_content_api, name='delete_game_content_api'),
    path('api/game-content/create/', views.create_game_content_api, name='create_game_content_api'),
    path('api/game-content/increment-usage/', views.increment_content_usage_api, name='increment_content_usage_api'),
]
