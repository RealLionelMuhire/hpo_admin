from django.urls import path
from . import views

app_name = 'hpo_app'

urlpatterns = [
    # API endpoints for questions
    path('api/questions/', views.questions_api, name='questions_api'),
    path('api/questions/<int:question_id>/', views.question_detail_api, name='question_detail_api'),
    path('api/packages/', views.packages_api, name='packages_api'),
    path('api/packages/<int:package_id>/questions/', views.package_questions_api, name='package_questions_api'),
]
