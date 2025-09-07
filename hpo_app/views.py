from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Question, QuestionPackage, Game, GameParticipant, GameResult, GameResponse, Player, GameContent, Topic, Subtopic
import json
import random
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum

# Helper function to avoid code duplication
def create_game_participant(game, player, team, is_winner, lost_card=None):
    """
    Helper function to create a game participant with proper marks allocation
    Returns the created participant instance
    """
    marks_earned = 1 if is_winner else 0  # Winners automatically get 1 mark
    
    participant = GameParticipant.objects.create(
        game=game,
        player=player,
        team=team,
        is_winner=is_winner,
        marks_earned=marks_earned,
        lost_card=lost_card if not is_winner else None,
        question_answered=False,  # Will be updated later for losers
        answer_correct=False      # Will be updated later for losers
    )
    
    # Update player's game statistics
    player.update_game_stats(
        won=is_winner,
        marks_earned=marks_earned,
        questions_answered=0,  # Will be updated separately for losers
        correct_answers=0      # Will be updated separately for losers
    )
    
    return participant

def generate_post_game_response(participant, lost_card=None):
    """
    Helper function to generate appropriate response for winners/losers
    Returns response data and creates GameResponse record
    """
    response_data = {}
    
    if participant.is_winner:
        # Winners get explanation (fun fact) from a question
        # Get random question explanation for winner
        all_questions = Question.objects.all()
        if all_questions.exists():
            random_question = all_questions.order_by('?').first()
            explanation_text = random_question.explanation
        else:
            explanation_text = 'Congratulations on your victory!'
            
        response_data = {
            'type': 'explanation',
            'explanation': explanation_text,
            'marks_earned': participant.marks_earned
        }
            
        # Create winner response in GameResponse model
        GameResponse.objects.create(
            game=participant.game,
            participant=participant,
            response_type='fun_fact',
            fun_fact_text=explanation_text
        )
        
    else:
        # Losers get full question object for their lost card
        if lost_card:
            questions = Question.objects.filter(card=lost_card)
            if questions.exists():
                question = questions.first()
                response_data = {
                    'type': 'question',
                    'question': {
                        'id': question.id,
                        'question_text': question.question_text,
                        'question_type': question.question_type,
                        'options': question.options,
                        'correct_answer': question.correct_answer,  # Frontend will validate
                        'explanation': question.explanation,
                        'points': question.points,
                        'difficulty': question.difficulty,
                        'card': question.card,
                        'card_info': question.get_card_info()
                    },
                    'instruction': 'Answer this question correctly to earn 1 mark'
                }
                
                # Create loser response in GameResponse model
                GameResponse.objects.create(
                    game=participant.game,
                    participant=participant,
                    response_type='question',
                    question=question
                )
            else:
                response_data = {
                    'type': 'no_question',
                    'message': f'No questions available for card {lost_card}'
                }
        else:
            response_data = {
                'type': 'no_card',
                'message': 'No card specified for loser'
            }
    
    return response_data

def finalize_game_if_complete(game):
    """
    Helper function to check if game is complete and finalize it
    Returns game status information
    """
    participants_submitted = game.participants.count()
    participants_expected = game.participant_count
    
    if participants_submitted >= participants_expected:
        game.status = 'completed'
        game.completed_at = timezone.now()
        
        # Determine winning team
        team1_winners = game.participants.filter(team=1, is_winner=True).count()
        team2_winners = game.participants.filter(team=2, is_winner=True).count()
        
        if team1_winners > team2_winners:
            game.winning_team = 1
        elif team2_winners > team1_winners:
            game.winning_team = 2
        # If tie, leave winning_team as None
        
        game.save()
        
        # Create or update game result
        team1_marks = game.participants.filter(team=1).aggregate(
            total=Sum('marks_earned'))['total'] or 0
        team2_marks = game.participants.filter(team=2).aggregate(
            total=Sum('marks_earned'))['total'] or 0
        
        GameResult.objects.get_or_create(
            game=game,
            defaults={
                'team1_marks': team1_marks,
                'team2_marks': team2_marks,
                'result_summary': {
                    'winning_team': game.winning_team,
                    'completed_at': game.completed_at.isoformat(),
                    'participants_count': participants_submitted
                }
            }
        )
    
    return {
        'participants_submitted': participants_submitted,
        'participants_expected': participants_expected,
        'status': game.status,
        'completed': participants_submitted >= participants_expected
    }

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def questions_by_card_api(request):
    """
    API endpoint to get questions by card for unauthenticated users
    POST payload: {"card": "S3"} or {"card": "HJ"} etc.
    """
    try:
        # Parse JSON payload
        data = json.loads(request.body)
        card = data.get('card')
        
        if not card:
            return JsonResponse({
                'success': False,
                'error': 'Card parameter is required in the payload'
            }, status=400)
        
        # Validate card format
        valid_cards = [choice[0] for choice in Question.CARD_CHOICES]
        if card not in valid_cards:
            return JsonResponse({
                'success': False,
                'error': f'Invalid card. Valid cards are: {", ".join(valid_cards)}'
            }, status=400)
        
        # Get questions for the specified card
        questions = Question.objects.filter(card=card)
        
        # Convert to JSON format
        questions_data = []
        for question in questions:
            question_data = {
                'id': question.id,
                'language': question.language,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'options': question.options,
                'correct_answer': question.correct_answer,
                'explanation': question.explanation,
                'points': question.points,
                'difficulty': question.difficulty,
                'card': question.card,
                'card_info': question.get_card_info(),
                'created_at': question.created_at.isoformat(),
            }
            questions_data.append(question_data)
        
        # Get card info for the requested card
        dummy_question = Question(card=card)
        card_info = dummy_question.get_card_info()
        
        return JsonResponse({
            'success': True,
            'card': card,
            'card_info': card_info,
            'count': len(questions_data),
            'questions': questions_data
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON payload'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

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
                'card': question.card,
                'card_info': question.get_card_info(),
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
            'card': question.card,
            'card_info': question.get_card_info(),
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
                'card': question.card,
                'card_info': question.get_card_info(),
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


# ==================== GAME API VIEWS ====================

@csrf_exempt
@require_http_methods(["POST"])
def create_game_api(request):
    """
    Create a new game session
    POST payload: {
        "participant_count": 2  # 1, 2, 4, or 6
    }
    
    NOTE: This endpoint now supports the new player-centric workflow.
    It creates a game with just the participant count and returns a match_id.
    Players will submit their own results individually using the match_id.
    """
    try:
        data = json.loads(request.body)
        participant_count = data.get('participant_count')
        
        # Validate participant count
        valid_counts = [1, 2, 4, 6]
        if participant_count not in valid_counts:
            return JsonResponse({
                'success': False,
                'error': f'Invalid participant count. Must be one of: {valid_counts}'
            }, status=400)
        
        # Create the game with just participant count
        # Players will be added when they submit their results
        game = Game.objects.create(
            participant_count=participant_count,
            team_count=2 if participant_count > 1 else 1,
            status='waiting'
        )
        
        return JsonResponse({
            'success': True,
            'game': {
                'match_id': str(game.match_id),
                'participant_count': game.participant_count,
                'team_count': game.team_count,
                'status': game.status,
                'created_at': game.created_at.isoformat() if game.created_at else None
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def complete_game_api(request):
    """
    Complete a game and set winners/losers
    POST payload: {
        "match_id": "uuid-string",
        "winning_team": 1,  # 1 or 2
        "cards_chosen": ["S3", "HJ"]  # cards chosen by losing team
    }
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        winning_team = data.get('winning_team')
        cards_chosen = data.get('cards_chosen', [])
        
        if not match_id:
            return JsonResponse({
                'success': False,
                'error': 'match_id is required'
            }, status=400)
        
        if winning_team not in [1, 2]:
            return JsonResponse({
                'success': False,
                'error': 'winning_team must be 1 or 2'
            }, status=400)
        
        # Validate cards_chosen if provided
        if cards_chosen:
            valid_cards = [choice[0] for choice in Question.CARD_CHOICES]
            invalid_cards = [card for card in cards_chosen if card not in valid_cards]
            if invalid_cards:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid cards: {", ".join(invalid_cards)}. Valid cards are: {", ".join(valid_cards)}'
                }, status=400)
        
        try:
            game = Game.objects.get(match_id=match_id, status='active')
        except Game.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Game not found or not active'
            }, status=404)
        
        with transaction.atomic():
            # Update game status
            game.status = 'completed'
            game.winning_team = winning_team
            game.cards_chosen = cards_chosen
            game.completed_at = timezone.now()
            game.save()
            
            # Update participants and their stats
            team1_marks = 0
            team2_marks = 0
            losing_players = []
            
            for participant in game.participants.all():
                if participant.team == winning_team:
                    participant.is_winner = True
                    participant.marks_earned = 1
                    if participant.team == 1:
                        team1_marks += 1
                    else:
                        team2_marks += 1
                    
                    # Update player game stats for winners
                    participant.player.update_game_stats(
                        won=True, 
                        marks_earned=1, 
                        questions_answered=0, 
                        correct_answers=0
                    )
                else:
                    participant.is_winner = False
                    participant.marks_earned = 0
                    losing_players.append(participant)
                    
                    # Update player game stats for losers (will be updated again when they answer question)
                    participant.player.update_game_stats(
                        won=False, 
                        marks_earned=0, 
                        questions_answered=0, 
                        correct_answers=0
                    )
                
                participant.save()
            
            # Assign cards to losing players
            if cards_chosen and losing_players:
                # If we have chosen cards, assign them to losing players
                for i, participant in enumerate(losing_players):
                    if i < len(cards_chosen):
                        participant.lost_card = cards_chosen[i]
                    else:
                        # If more losers than cards, cycle through the cards
                        participant.lost_card = cards_chosen[i % len(cards_chosen)]
                    participant.save()
            elif losing_players:
                # If no cards chosen, assign random cards to losing players
                all_cards = [choice[0] for choice in Question.CARD_CHOICES]
                for participant in losing_players:
                    participant.lost_card = random.choice(all_cards)
                    participant.save()
            
            # Create game result
            GameResult.objects.create(
                game=game,
                team1_marks=team1_marks,
                team2_marks=team2_marks,
                result_summary={
                    'winning_team': winning_team,
                    'cards_chosen': cards_chosen,
                    'completed_at': timezone.now().isoformat()
                }
            )
            
            return JsonResponse({
                'success': True,
                'game': {
                    'match_id': str(game.match_id),
                    'status': game.status,
                    'winning_team': game.winning_team,
                    'team1_marks': team1_marks,
                    'team2_marks': team2_marks,
                    'completed_at': game.completed_at.isoformat() if game.completed_at else None
                }
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_game_responses_api(request, match_id):
    """
    Get responses for players after game completion
    Winners get fun facts, losers get questions to answer
    """
    try:
        try:
            game = Game.objects.get(match_id=match_id, status='completed')
        except Game.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Game not found or not completed'
            }, status=404)
        
        responses_data = []
        
        for participant in game.participants.all():
            if participant.is_winner:
                # Winner gets fun fact from chosen cards
                fun_fact_card = None
                fun_fact_text = "Congratulations on winning!"
                
                # Try to get fun fact from chosen cards
                if game.cards_chosen:
                    for card in game.cards_chosen:
                        card_questions = Question.objects.filter(
                            card=card,
                            explanation__isnull=False
                        ).exclude(explanation='')
                        
                        if card_questions.exists():
                            question = card_questions.first()
                            fun_fact_text = question.explanation
                            fun_fact_card = card
                            break
                
                # Create response record
                response, created = GameResponse.objects.get_or_create(
                    game=game,
                    participant=participant,
                    defaults={
                        'response_type': 'fun_fact',
                        'fun_fact_text': fun_fact_text,
                        'fun_fact_card': fun_fact_card
                    }
                )
                
                responses_data.append({
                    'username': participant.player.username,
                    'player_name': participant.player.player_name,
                    'team': participant.team,
                    'is_winner': True,
                    'response_type': 'fun_fact',
                    'fun_fact': fun_fact_text,
                    'card': fun_fact_card,
                    'card_info': Question(card=fun_fact_card).get_card_info() if fun_fact_card else None
                })
            
            else:
                # Loser gets question related to their assigned card
                if participant.lost_card:
                    card_questions = Question.objects.filter(card=participant.lost_card)
                    if card_questions.exists():
                        question = random.choice(card_questions)
                        
                        # Create response record
                        response, created = GameResponse.objects.get_or_create(
                            game=game,
                            participant=participant,
                            defaults={
                                'response_type': 'question',
                                'question': question
                            }
                        )
                        
                        responses_data.append({
                            'username': participant.player.username,
                            'player_name': participant.player.player_name,
                            'team': participant.team,
                            'is_winner': False,
                            'response_type': 'question',
                            'card': participant.lost_card,
                            'card_info': question.get_card_info(),
                            'question': {
                                'id': question.id,
                                'language': question.language,
                                'question_text': question.question_text,
                                'question_type': question.question_type,
                                'options': question.options,
                                'difficulty': question.difficulty,
                                'points': question.points
                            }
                        })
                    else:
                        responses_data.append({
                            'username': participant.player.username,
                            'player_name': participant.player.player_name,
                            'team': participant.team,
                            'is_winner': False,
                            'response_type': 'question',
                            'card': participant.lost_card,
                            'card_info': Question(card=participant.lost_card).get_card_info(),
                            'question': None,
                            'message': 'No questions available for this card'
                        })
                else:
                    responses_data.append({
                        'username': participant.player.username,
                        'player_name': participant.player.player_name,
                        'team': participant.team,
                        'is_winner': False,
                        'response_type': 'question',
                        'card': None,
                        'card_info': None,
                        'question': None,
                        'message': 'No card assigned'
                    })
        
        return JsonResponse({
            'success': True,
            'game': {
                'match_id': str(game.match_id),
                'status': game.status,
                'winning_team': game.winning_team
            },
            'responses': responses_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_answer_api(request):
    """
    Submit answer for a question (for losing players)
    POST payload: {
        "match_id": "uuid-string",
        "username": "player1",
        "answer": "option text or True/False"
    }
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        username = data.get('username')
        answer = data.get('answer')
        
        if not all([match_id, username, answer]):
            return JsonResponse({
                'success': False,
                'error': 'match_id, username, and answer are required'
            }, status=400)
        
        try:
            game = Game.objects.get(match_id=match_id, status='completed')
            participant = game.participants.get(player__username=username, is_winner=False)
            response = GameResponse.objects.get(
                game=game,
                participant=participant,
                response_type='question'
            )
        except (Game.DoesNotExist, GameParticipant.DoesNotExist, GameResponse.DoesNotExist):
            return JsonResponse({
                'success': False,
                'error': 'Game, participant, or response not found'
            }, status=404)
        
        if response.question:
            # Check if answer is correct
            is_correct = (answer.strip() == response.question.correct_answer.strip())
            
            # Update response
            response.player_answer = answer
            response.is_correct = is_correct
            response.save()
            
            # Update participant
            participant.question_answered = True
            participant.answer_correct = is_correct
            participant.save()
            
            # Update player's question answering statistics
            current_correct = participant.player.correct_answers
            current_total = participant.player.questions_answered
            
            participant.player.questions_answered = current_total + 1
            if is_correct:
                participant.player.correct_answers = current_correct + 1
            participant.player.save()
            
            return JsonResponse({
                'success': True,
                'result': {
                    'is_correct': is_correct,
                    'correct_answer': response.question.correct_answer,
                    'explanation': response.question.explanation,
                    'points_earned': response.question.points if is_correct else 0
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No question found for this participant'
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_game_status_api(request, match_id):
    """
    Get current game status and information
    """
    try:
        try:
            game = Game.objects.get(match_id=match_id)
        except Game.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Game not found'
            }, status=404)
        
        participants_data = []
        for participant in game.participants.all():
            participant_data = {
                'username': participant.player.username,
                'player_name': participant.player.player_name,
                'team': participant.team,
                'is_winner': participant.is_winner,
                'marks_earned': participant.marks_earned,
                'lost_card': participant.lost_card,
                'question_answered': participant.question_answered,
                'answer_correct': participant.answer_correct
            }
            participants_data.append(participant_data)
        
        game_data = {
            'match_id': str(game.match_id),
            'participant_count': game.participant_count,
            'team_count': game.team_count,
            'status': game.status,
            'winning_team': game.winning_team,
            'cards_chosen': game.cards_chosen,
            'created_at': game.created_at.isoformat(),
            'completed_at': game.completed_at.isoformat() if game.completed_at else None,
            'participants': participants_data
        }
        
        # Add result information if game is completed
        if game.status == 'completed':
            try:
                result = game.result
                game_data['result'] = {
                    'team1_marks': result.team1_marks,
                    'team2_marks': result.team2_marks,
                    'result_summary': result.result_summary
                }
            except GameResult.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'game': game_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_player_stats_api(request, username):
    """
    Get player's game statistics and history
    """
    try:
        try:
            player = Player.objects.get(username=username)
        except Player.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Player not found'
            }, status=404)
        
        # Get recent games
        recent_games = GameParticipant.objects.filter(
            player=player
        ).select_related('game').order_by('-joined_at')[:10]
        
        recent_games_data = []
        for participation in recent_games:
            game_data = {
                'match_id': str(participation.game.match_id),
                'date': participation.joined_at.isoformat(),
                'participants': participation.game.participant_count,
                'team': participation.team,
                'won': participation.is_winner,
                'marks_earned': participation.marks_earned,
                'card_assigned': participation.lost_card,
                'question_answered': participation.question_answered,
                'answer_correct': participation.answer_correct,
                'game_status': participation.game.status
            }
            recent_games_data.append(game_data)
        
        return JsonResponse({
            'success': True,
            'player': {
                'username': player.username,
                'player_name': player.player_name,
                'created_at': player.created_at.isoformat(),
                'last_active': player.updated_at.isoformat()
            },
            'statistics': player.get_game_history_summary(),
            'recent_games': recent_games_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_leaderboard_api(request):
    """
    Get player leaderboard based on various metrics
    Query parameters:
    - metric: 'win_rate', 'total_marks', 'games_won', 'answer_accuracy', 'win_streak'
    - limit: number of players to return (default 10)
    """
    try:
        metric = request.GET.get('metric', 'total_marks')
        limit = int(request.GET.get('limit', 10))
        
        # Validate metric
        valid_metrics = ['win_rate', 'total_marks', 'games_won', 'answer_accuracy', 'win_streak']
        if metric not in valid_metrics:
            return JsonResponse({
                'success': False,
                'error': f'Invalid metric. Valid options: {", ".join(valid_metrics)}'
            }, status=400)
        
        # Order players based on metric
        if metric == 'win_rate':
            # For win rate, we need players who have played at least 1 game
            players = Player.objects.filter(games_played__gt=0).order_by('-games_won', '-games_played')[:limit]
        elif metric == 'total_marks':
            players = Player.objects.filter(games_played__gt=0).order_by('-total_game_marks')[:limit]
        elif metric == 'games_won':
            players = Player.objects.filter(games_played__gt=0).order_by('-games_won')[:limit]
        elif metric == 'answer_accuracy':
            players = Player.objects.filter(questions_answered__gt=0).order_by('-correct_answers', '-questions_answered')[:limit]
        elif metric == 'win_streak':
            players = Player.objects.filter(games_played__gt=0).order_by('-longest_win_streak')[:limit]
        
        leaderboard_data = []
        for i, player in enumerate(players, 1):
            player_data = {
                'rank': i,
                'username': player.username,
                'player_name': player.player_name,
                'games_played': player.games_played,
                'games_won': player.games_won,
                'total_marks': player.total_game_marks,
                'win_rate': player.win_rate,
                'answer_accuracy': player.answer_accuracy,
                'current_win_streak': player.current_win_streak,
                'longest_win_streak': player.longest_win_streak,
                'last_played': player.last_game_played.isoformat() if player.last_game_played else None
            }
            leaderboard_data.append(player_data)
        
        return JsonResponse({
            'success': True,
            'metric': metric,
            'total_players': len(leaderboard_data),
            'leaderboard': leaderboard_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_card_questions_api(request, card_id):
    """
    Get questions associated with a specific card
    GET /api/cards/{card_id}/questions/
    """
    try:
        # Validate card format
        valid_cards = [choice[0] for choice in Question.CARD_CHOICES]
        if card_id not in valid_cards:
            return JsonResponse({
                'success': False,
                'error': f'Invalid card. Valid cards are: {", ".join(valid_cards)}'
            }, status=400)
        
        # Get questions for the specified card
        questions = Question.objects.filter(card=card_id)
        
        if not questions.exists():
            return JsonResponse({
                'success': False,
                'error': f'No questions found for card {card_id}'
            }, status=404)
        
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
                'card': question.card,
                'card_info': question.get_card_info(),
                'created_at': question.created_at.isoformat()
            }
            questions_data.append(question_data)
        
        # Get card info
        card_info = Question(card=card_id).get_card_info()
        
        return JsonResponse({
            'success': True,
            'card': card_id,
            'card_info': card_info,
            'count': len(questions_data),
            'questions': questions_data
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def award_points_api(request):
    """
    Award points to a player after frontend validates correct answer
    Used specifically for losers who answered questions correctly
    POST payload: {
        "match_id": "uuid-string",
        "username": "player1",
        "question_id": 123,
        "answer": "correct_answer",
        "points": 1
    }
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        username = data.get('username')
        question_id = data.get('question_id')
        answer = data.get('answer')
        points = data.get('points', 1)  # Default to 1 point
        
        if not all([match_id, username, question_id, answer]):
            return JsonResponse({
                'success': False,
                'error': 'match_id, username, question_id, and answer are required'
            }, status=400)
        
        try:
            game = Game.objects.get(match_id=match_id)
            participant = game.participants.get(player__username=username, is_winner=False)
            question = Question.objects.get(id=question_id)
            
            # Verify the answer is actually correct (security check)
            if answer.strip().lower() != question.correct_answer.strip().lower():
                return JsonResponse({
                    'success': False,
                    'error': 'Answer is not correct'
                }, status=400)
            
            # Check if already answered to prevent duplicate points
            if participant.question_answered and participant.answer_correct:
                return JsonResponse({
                    'success': False,
                    'error': 'Player has already answered this question correctly'
                }, status=400)
            
            with transaction.atomic():
                # Update participant with correct answer and award marks
                participant.question_answered = True
                participant.answer_correct = True
                participant.marks_earned += points  # Add the earned mark
                participant.save()
                
                # Update or create game response
                response, created = GameResponse.objects.get_or_create(
                    game=game,
                    participant=participant,
                    response_type='question',
                    defaults={
                        'question': question,
                        'player_answer': answer,
                        'is_correct': True
                    }
                )
                
                if not created:
                    # Update existing response
                    response.player_answer = answer
                    response.is_correct = True
                    response.save()
                
                # Update player's overall statistics
                player = participant.player
                player.total_game_marks += points
                player.questions_answered += 1
                player.correct_answers += 1
                player.save()
                
                # Update game result marks
                game_result = GameResult.objects.get(game=game)
                if participant.team == 1:
                    game_result.team1_marks += points
                else:
                    game_result.team2_marks += points
                game_result.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Awarded {points} point(s) to {username} for correct answer',
                'result': {
                    'points_awarded': points,
                    'player': {
                        'username': username,
                        'total_marks': participant.marks_earned,
                        'total_correct_answers': player.correct_answers,
                        'total_questions_answered': player.questions_answered,
                        'answer_accuracy': round((player.correct_answers / player.questions_answered) * 100, 2) if player.questions_answered > 0 else 0
                    },
                    'question': {
                        'id': question.id,
                        'explanation': question.explanation,
                        'points': question.points
                    }
                }
            })
            
        except Game.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Game with match_id {match_id} not found'
            }, status=404)
        except GameParticipant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Player {username} not found as a loser in this game'
            }, status=404)
        except Question.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Question with ID {question_id} not found'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON payload'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def record_wrong_answer_api(request):
    """
    Record a wrong answer (no points awarded)
    POST payload: {
        "match_id": "uuid-string",
        "username": "player1",
        "question_id": 123,
        "answer": "wrong_answer"
    }
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        username = data.get('username')
        question_id = data.get('question_id')
        answer = data.get('answer')
        
        if not all([match_id, username, question_id, answer]):
            return JsonResponse({
                'success': False,
                'error': 'match_id, username, question_id, and answer are required'
            }, status=400)
        
        try:
            game = Game.objects.get(match_id=match_id, status='completed')
            participant = game.participants.get(player__username=username, is_winner=False)
            question = Question.objects.get(id=question_id)
            
            # Check if response already exists, if not create one
            response, created = GameResponse.objects.get_or_create(
                game=game,
                participant=participant,
                response_type='question',
                defaults={
                    'question': question,
                    'player_answer': answer,
                    'is_correct': False
                }
            )
            
            if not created:
                # Update existing response
                response.player_answer = answer
                response.is_correct = False
                response.save()
            
            # Update participant
            participant.question_answered = True
            participant.answer_correct = False
            participant.save()
            
            # Update player's question answering statistics
            with transaction.atomic():
                current_total = participant.player.questions_answered
                participant.player.questions_answered = current_total + 1
                participant.player.save()
            
            return JsonResponse({
                'success': True,
                'result': {
                    'points_awarded': 0,
                    'correct_answer': question.correct_answer,
                    'explanation': question.explanation,
                    'player': {
                        'username': username,
                        'total_correct_answers': participant.player.correct_answers,
                        'total_questions_answered': participant.player.questions_answered,
                        'answer_accuracy': round((participant.player.correct_answers / participant.player.questions_answered) * 100, 2) if participant.player.questions_answered > 0 else 0
                    }
                }
            })
            
        except (Game.DoesNotExist, GameParticipant.DoesNotExist, Question.DoesNotExist) as e:
            return JsonResponse({
                'success': False,
                'error': f'Game, participant, or question not found: {str(e)}'
            }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_completed_game_api(request):
    """
    Submit a completed game from UI with simplified player-centric workflow
    POST payload: {
        "match_id": "uuid-string",
        "player_id": 1,
        "username": "alice",
        "team": 1,
        "is_winner": true,
        "lost_card": null  # Only for losers
    }
    
    Post-game logic:
    - Winners: Automatically get 1 mark and receive explanation (fun fact) from question model
    - Losers: Get full question object, frontend validates answer, then calls award-points endpoint
    - No more "question_answered" or "answer_correct" fields needed for winners
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        player_id = data.get('player_id')
        username = data.get('username')
        is_winner = data.get('is_winner')
        team = data.get('team')
        lost_card = data.get('lost_card')
        
        # Validate required fields
        required_fields = ['match_id', 'player_id', 'username', 'team', 'is_winner']
        missing_fields = [field for field in required_fields if data.get(field) is None]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
            
        # Validate lost_card if provided
        if lost_card:
            valid_cards = [choice[0] for choice in Question.CARD_CHOICES]
            if lost_card not in valid_cards:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid lost_card: {lost_card}. Valid cards are: {", ".join(valid_cards)}'
                }, status=400)

        with transaction.atomic():
            # Get the game
            try:
                game = Game.objects.get(match_id=match_id)
            except Game.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f'Game with match_id {match_id} not found'
                }, status=404)
            
            # Get the player
            try:
                player = Player.objects.get(id=player_id)
                # Update username if provided
                if player.username != username:
                    player.username = username
                    player.save()
            except Player.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f'Player with ID {player_id} not found'
                }, status=400)
            
            # Check if player already submitted for this game
            existing_participant = GameParticipant.objects.filter(game=game, player=player).first()
            if existing_participant:
                return JsonResponse({
                    'success': False,
                    'error': f'Player {username} has already submitted result for this game'
                }, status=400)
            
            # Create game participant using helper function
            participant = create_game_participant(
                game=game,
                player=player,
                team=team,
                is_winner=is_winner,
                lost_card=lost_card
            )
            
            # Generate appropriate response using helper function
            response_data = generate_post_game_response(participant, lost_card)
            
            # Check if all participants have submitted and finalize game
            game_status = finalize_game_if_complete(game)
            
            return JsonResponse({
                'success': True,
                'message': 'Game result submitted successfully',
                'player': {
                    'player_id': player.id,
                    'username': player.username,
                    'team': participant.team,
                    'is_winner': participant.is_winner,
                    'marks_earned': participant.marks_earned
                },
                'response': response_data,
                'game_status': {
                    'match_id': str(game.match_id),
                    **game_status
                }
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ==================== GAME CONTENT API ENDPOINTS ====================

@csrf_exempt
@require_http_methods(["GET"])
def get_game_content_api(request):
    """
    API endpoint to get game content with filtering options
    GET /api/game-content/?language=english&age_group=15-19&topic=history
    """
    try:
        # Get query parameters
        language = request.GET.get('language')
        age_group = request.GET.get('age_group')
        topic = request.GET.get('topic')
        subtopic = request.GET.get('subtopic')
        content_type = request.GET.get('content_type')
        status = request.GET.get('status', 'published')  # Default to published
        
        # Start with published content only (unless specified otherwise)
        content_queryset = GameContent.objects.filter(status=status)
        
        # Apply filters
        if language:
            content_queryset = content_queryset.filter(language=language)
        if age_group:
            content_queryset = content_queryset.filter(age_group=age_group)
        if topic:
            content_queryset = content_queryset.filter(topic__icontains=topic)
        if subtopic:
            content_queryset = content_queryset.filter(subtopic__icontains=subtopic)
        if content_type:
            content_queryset = content_queryset.filter(content_type=content_type)
        
        # Order by creation date (most recent first)
        content_queryset = content_queryset.order_by('-created_at')
        
        # Convert to JSON format
        content_data = []
        for content in content_queryset:
            content_data.append({
                'id': content.id,
                'title': content.title,
                'language': content.language,
                'age_group': content.age_group,
                'topic': content.topic,
                'subtopic': content.subtopic,
                'all_subtopics': content.get_all_subtopics(),
                'subtopics_count': content.get_subtopics_count(),
                'hierarchy': content.get_hierarchy_display(),
                'info': content.info,
                'content_type': content.content_type,
                'difficulty_level': content.difficulty_level,
                'status': content.status,
                'tags': content.get_tags_list(),
                'card_association': content.card_association,
                'view_count': content.view_count,
                'usage_count': content.usage_count,
                'created_at': content.created_at.isoformat(),
                'updated_at': content.updated_at.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'count': len(content_data),
            'filters_applied': {
                'language': language,
                'age_group': age_group,
                'topic': topic,
                'subtopic': subtopic,
                'content_type': content_type,
                'status': status
            },
            'content': content_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_game_content_detail_api(request, content_id):
    """
    API endpoint to get detailed information about specific game content
    GET /api/game-content/{content_id}/
    """
    try:
        content = GameContent.objects.get(id=content_id)
        
        # Increment view count
        content.increment_view_count()
        
        # Prepare detailed response
        content_data = {
            'id': content.id,
            'title': content.title,
            'language': content.language,
            'age_group': content.age_group,
            'topic': content.topic,
            'subtopic': content.subtopic,
            'all_subtopics': content.get_all_subtopics(),
            'subtopics_count': content.get_subtopics_count(),
            'hierarchy': content.get_hierarchy_display(),
            'info': content.info,
            'content_type': content.content_type,
            'difficulty_level': content.difficulty_level,
            'status': content.status,
            'tags': content.get_tags_list(),
            'card_association': content.card_association,
            'view_count': content.view_count,
            'usage_count': content.usage_count,
            'created_at': content.created_at.isoformat(),
            'updated_at': content.updated_at.isoformat(),
            'published_at': content.published_at.isoformat() if content.published_at else None
        }
        
        # Add creator information if available
        if content.created_by:
            content_data['created_by'] = {
                'name': content.created_by.name,
                'email': content.created_by.email
            }
        
        # Add approver information if available
        if content.approved_by:
            content_data['approved_by'] = {
                'name': content.approved_by.name,
                'email': content.approved_by.email
            }
        
        # Add related question if available
        if content.related_question:
            content_data['related_question'] = {
                'id': content.related_question.id,
                'question_text': content.related_question.question_text,
                'card': content.related_question.card
            }
        
        return JsonResponse({
            'success': True,
            'content': content_data
        })
        
    except GameContent.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Game content not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_game_content_by_language_age_api(request, language, age_group):
    """
    API endpoint to get game content filtered by language and age group
    GET /api/game-content/{language}/{age_group}/
    """
    try:
        # Filter by language and age group
        contents = GameContent.objects.filter(
            language=language,
            age_group=age_group,
            status='published'
        ).order_by('-created_at')
        
        # Apply additional filters
        topic = request.GET.get('topic', '')
        if topic:
            contents = contents.filter(topic__icontains=topic)
        
        difficulty = request.GET.get('difficulty', '')
        if difficulty:
            contents = contents.filter(difficulty_level=difficulty)
        
        # Prepare response data
        contents_data = []
        for content in contents:
            content_data = {
                'id': content.id,
                'title': content.title,
                'language': content.language,
                'age_group': content.age_group,
                'topic': content.topic,
                'subtopic': content.subtopic,
                'info': content.info,
                'content_type': content.content_type,
                'difficulty_level': content.difficulty_level,
                'status': content.status,
                'tags': content.get_tags_list(),
                'usage_count': content.usage_count,
                'view_count': content.view_count,
                'created_at': content.created_at.isoformat()
            }
            contents_data.append(content_data)
        
        return JsonResponse({
            'success': True,
            'count': len(contents_data),
            'filters': {
                'language': language,
                'age_group': age_group,
                'topic': topic,
                'difficulty': difficulty
            },
            'contents': contents_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_game_content_api(request):
    """
    API endpoint to create new game content
    POST /api/game-content/create/
    """
    try:
        data = json.loads(request.body)
        
        # Required fields
        required_fields = ['language', 'age_group', 'topic', 'subtopic', 'info']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Required field missing: {field}'
                }, status=400)
        
        # Validate choices
        valid_languages = [choice[0] for choice in GameContent.LANGUAGE_CHOICES]
        valid_age_groups = [choice[0] for choice in GameContent.AGE_GROUP_CHOICES]
        valid_content_types = [choice[0] for choice in GameContent.CONTENT_TYPE_CHOICES]
        
        if data['language'] not in valid_languages:
            return JsonResponse({
                'success': False,
                'error': f'Invalid language. Valid options: {", ".join(valid_languages)}'
            }, status=400)
        
        if data['age_group'] not in valid_age_groups:
            return JsonResponse({
                'success': False,
                'error': f'Invalid age group. Valid options: {", ".join(valid_age_groups)}'
            }, status=400)
        
        # Create new game content
        content = GameContent.objects.create(
            language=data['language'],
            age_group=data['age_group'],
            topic=data['topic'],
            subtopic=data['subtopic'],
            info=data['info'],
            title=data.get('title', ''),
            content_type=data.get('content_type', 'educational'),
            difficulty_level=data.get('difficulty_level', 'beginner'),
            status=data.get('status', 'draft'),
            tags=data.get('tags', ''),
            card_association=data.get('card_association', ''),
            subtopics_data=data.get('subtopics_data', []),
        )
        
        return JsonResponse({
            'success': True,
            'content': {
                'id': content.id,
                'title': content.title,
                'language': content.language,
                'age_group': content.age_group,
                'topic': content.topic,
                'subtopic': content.subtopic,
                'all_subtopics': content.get_all_subtopics(),
                'subtopics_count': content.get_subtopics_count(),
                'info': content.info,
                'content_type': content.content_type,
                'difficulty_level': content.difficulty_level,
                'status': content.status,
                'tags': content.tags,
                'created_at': content.created_at.isoformat()
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_game_content_api(request, content_id):
    """
    API endpoint to update existing game content
    PUT /api/game-content/<id>/update/
    """
    try:
        content = GameContent.objects.get(id=content_id)
        data = json.loads(request.body)
        
        # Validate language if provided
        if 'language' in data:
            valid_languages = [choice[0] for choice in GameContent.LANGUAGE_CHOICES]
            if data['language'] not in valid_languages:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid language. Valid options: {", ".join(valid_languages)}'
                }, status=400)
            content.language = data['language']
        
        # Validate choices
        if 'age_group' in data:
            valid_age_groups = [choice[0] for choice in GameContent.AGE_GROUP_CHOICES]
            if data['age_group'] not in valid_age_groups:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid age group. Valid options: {", ".join(valid_age_groups)}'
                }, status=400)
            content.age_group = data['age_group']
        
        if 'content_type' in data:
            valid_content_types = [choice[0] for choice in GameContent.CONTENT_TYPE_CHOICES]
            if data['content_type'] not in valid_content_types:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid content type. Valid options: {", ".join(valid_content_types)}'
                }, status=400)
            content.content_type = data['content_type']
        
        # Update other fields
        for field in ['title', 'topic', 'subtopic', 'info', 'difficulty_level', 'status', 'tags', 'card_association']:
            if field in data:
                setattr(content, field, data[field])
        
        # Handle subtopics_data update
        if 'subtopics_data' in data:
            content.subtopics_data = data['subtopics_data']
        
        content.save()
        
        return JsonResponse({
            'success': True,
            'content': {
                'id': content.id,
                'title': content.title,
                'language': content.language,
                'age_group': content.age_group,
                'topic': content.topic,
                'subtopic': content.subtopic,
                'info': content.info,
                'content_type': content.content_type,
                'difficulty_level': content.difficulty_level,
                'status': content.status,
                'tags': content.tags,
                'updated_at': content.updated_at.isoformat()
            }
        })
        
    except GameContent.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Game content not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_game_content_api(request, content_id):
    """
    API endpoint to delete game content
    DELETE /api/game-content/<id>/delete/
    """
    try:
        content = GameContent.objects.get(id=content_id)
        content.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Game content deleted successfully'
        })
        
    except GameContent.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Game content not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def increment_content_usage_api(request):
    """
    API endpoint to increment usage count for game content
    POST /api/game-content/increment-usage/
    """
    try:
        data = json.loads(request.body)
        content_id = data.get('content_id')
        
        if not content_id:
            return JsonResponse({
                'success': False,
                'error': 'content_id is required'
            }, status=400)
        
        content = GameContent.objects.get(id=content_id)
        content.increment_usage_count()
        
        return JsonResponse({
            'success': True,
            'content': {
                'id': content.id,
                'title': content.title,
                'usage_count': content.usage_count,
                'view_count': content.view_count
            }
        })
        
    except GameContent.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Game content not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_player_result_api(request):
    """
    Submit individual player result for a game
    POST payload: {
        "match_id": "uuid-string",
        "player_id": 1,
        "username": "alice",
        "player_name": "Alice", 
        "team": 1,
        "marks_earned": 1,
        "is_winner": true,
        "lost_card": null,
        "question_answered": false,
        "answer_correct": false
    }
    
    This endpoint supports the new player-centric workflow where each player
    individually submits their game result using the shared match_id.
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        player_id = data.get('player_id')
        username = data.get('username')
        
        # Validate required fields
        required_fields = ['match_id', 'player_id', 'username', 'team', 'is_winner']
        missing_fields = [field for field in required_fields if data.get(field) is None]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
        
        # Get or create the game
        try:
            game = Game.objects.get(match_id=match_id)
        except Game.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Game with match_id {match_id} not found'
            }, status=404)
        
        # Get or create the player
        try:
            player = Player.objects.get(id=player_id)
            # Update player info if provided
            if player.username != username:
                player.username = username
            if data.get('player_name') and player.player_name != data['player_name']:
                player.player_name = data['player_name']
            player.save()
        except Player.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Player with ID {player_id} not found'
            }, status=400)
        
        # Check if player already submitted for this game
        existing_participant = GameParticipant.objects.filter(game=game, player=player).first()
        if existing_participant:
            return JsonResponse({
                'success': False,
                'error': f'Player {username} has already submitted result for this game'
            }, status=400)
        
        with transaction.atomic():
            # Create game participant using helper function
            participant = create_game_participant(
                game=game,
                player=player,
                team=data['team'],
                is_winner=data['is_winner'],
                lost_card=data.get('lost_card')
            )
            
            # Generate appropriate response using helper function
            response_data = generate_post_game_response(participant, data.get('lost_card'))
            
            # Check if all participants have submitted and finalize game
            game_status = finalize_game_if_complete(game)
            
            return JsonResponse({
                'success': True,
                'message': 'Player result submitted successfully',
                'player': {
                    'player_id': player.id,
                    'username': player.username,
                    'player_name': player.player_name,
                    'team': participant.team,
                    'is_winner': participant.is_winner,
                    'marks_earned': participant.marks_earned
                },
                'response': response_data,
                'game_status': {
                    'match_id': str(game.match_id),
                    **game_status
                }
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)