from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Question, QuestionPackage
import json

# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
def questions_api(request):
    """
    API endpoint to get questions as JSON for unauthenticated users
    """
    try:
        # Get all questions
        questions = Question.objects.all()
        
        # Convert to JSON format
        questions_data = []
        for question in questions:
            question_data = {
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'options': question.options,
                'correct_answer': question.correct_answer,
                'explanation': question.explanation,
                'points': question.points,
                'difficulty': question.difficulty,
                'created_at': question.created_at.isoformat(),
            }
            questions_data.append(question_data)
        
        return JsonResponse({
            'success': True,
            'count': len(questions_data),
            'questions': questions_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def question_detail_api(request, question_id):
    """
    API endpoint to get a specific question by ID
    """
    try:
        question = Question.objects.get(id=question_id)
        
        question_data = {
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'options': question.options,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'points': question.points,
            'difficulty': question.difficulty,
            'created_at': question.created_at.isoformat(),
        }
        
        return JsonResponse({
            'success': True,
            'question': question_data
        })
    
    except Question.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Question not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def packages_api(request):
    """
    API endpoint to get question packages as JSON
    """
    try:
        # Get published packages only
        packages = QuestionPackage.objects.filter(status='published')
        
        packages_data = []
        for package in packages:
            package_data = {
                'id': package.id,
                'name': package.name,
                'description': package.description,
                'type': package.type,
                'category': package.category,
                'visibility': package.visibility,
                'difficulty': package.difficulty,
                'estimated_duration': package.estimated_duration,
                'language': package.language,
                'tags': package.tags,
                'total_attempts': package.total_attempts,
                'average_score': float(package.average_score),
                'completion_rate': float(package.completion_rate),
                'created_at': package.created_at.isoformat(),
                'question_count': package.questions.count()
            }
            packages_data.append(package_data)
        
        return JsonResponse({
            'success': True,
            'count': len(packages_data),
            'packages': packages_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def package_questions_api(request, package_id):
    """
    API endpoint to get questions from a specific package
    """
    try:
        package = QuestionPackage.objects.get(id=package_id, status='published')
        questions = package.questions.all()
        
        questions_data = []
        for question in questions:
            question_data = {
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'options': question.options,
                'correct_answer': question.correct_answer,
                'explanation': question.explanation,
                'points': question.points,
                'difficulty': question.difficulty,
            }
            questions_data.append(question_data)
        
        return JsonResponse({
            'success': True,
            'package': {
                'id': package.id,
                'name': package.name,
                'description': package.description,
                'difficulty': package.difficulty,
                'estimated_duration': package.estimated_duration,
            },
            'count': len(questions_data),
            'questions': questions_data
        })
    
    except QuestionPackage.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Package not found or not published'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
