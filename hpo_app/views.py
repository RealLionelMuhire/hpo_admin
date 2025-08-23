from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Question, QuestionPackage, Game, GameParticipant, GameResult, GameResponse, Player
import json
import random
from django.utils import timezone
from django.db import transaction

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
        "participant_count": 2,  # 1, 2, 4, or 6
        "players": [
            {"username": "player1", "player_name": "Player One"},
            {"username": "player2", "player_name": "Player Two"}
        ]
    }
    """
    try:
        data = json.loads(request.body)
        participant_count = data.get('participant_count')
        players_data = data.get('players', [])
        
        # Validate participant count
        valid_counts = [1, 2, 4, 6]
        if participant_count not in valid_counts:
            return JsonResponse({
                'success': False,
                'error': f'Invalid participant count. Must be one of: {valid_counts}'
            }, status=400)
        
        # For single player game, no players array needed
        if participant_count == 1:
            if len(players_data) != 1:
                return JsonResponse({
                    'success': False,
                    'error': 'Single player game requires exactly 1 player'
                }, status=400)
        else:
            if len(players_data) != participant_count:
                return JsonResponse({
                    'success': False,
                    'error': f'Number of players ({len(players_data)}) must match participant count ({participant_count})'
                }, status=400)
        
        with transaction.atomic():
            # Create the game
            game = Game.objects.create(
                participant_count=participant_count,
                status='waiting'
            )
            
            # Create or get players and add them to the game
            for i, player_data in enumerate(players_data):
                username = player_data.get('username')
                player_name = player_data.get('player_name', username)
                
                if not username:
                    return JsonResponse({
                        'success': False,
                        'error': 'Username is required for each player'
                    }, status=400)
                
                # Get or create player (for unauthenticated system)
                player, created = Player.objects.get_or_create(
                    username=username,
                    defaults={
                        'player_name': player_name,
                        'password': 'temp123'  # Temporary password for unauthenticated players
                    }
                )
                
                # Assign team (for 1 player game, always team 1)
                if participant_count == 1:
                    team = 1
                else:
                    team = 1 if i < participant_count // 2 else 2
                
                # Create game participant
                GameParticipant.objects.create(
                    game=game,
                    player=player,
                    team=team
                )
            
            # Set game status to active
            game.status = 'active'
            game.save()
            
            return JsonResponse({
                'success': True,
                'game': {
                    'match_id': str(game.match_id),
                    'participant_count': game.participant_count,
                    'team_count': game.team_count,
                    'players_per_team': game.players_per_team,
                    'status': game.status,
                    'participants': [
                        {
                            'username': p.player.username,
                            'player_name': p.player.player_name,
                            'team': p.team
                        }
                        for p in game.participants.all()
                    ]
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
        "cards_played": ["S3", "HJ", "DA"]  # optional
    }
    """
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        winning_team = data.get('winning_team')
        cards_played = data.get('cards_played', [])
        
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
            game.cards_in_play = cards_played
            game.completed_at = timezone.now()
            game.save()
            
            # Update participants and their stats
            team1_marks = 0
            team2_marks = 0
            
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
                    # Assign a random card for the losing player
                    if cards_played:
                        participant.lost_card = random.choice(cards_played)
                    else:
                        # Pick a random card if none specified
                        all_cards = [choice[0] for choice in Question.CARD_CHOICES]
                        participant.lost_card = random.choice(all_cards)
                    
                    # Update player game stats for losers (will be updated again when they answer question)
                    participant.player.update_game_stats(
                        won=False, 
                        marks_earned=0, 
                        questions_answered=0, 
                        correct_answers=0
                    )
                
                participant.save()
            
            # Create game result
            GameResult.objects.create(
                game=game,
                team1_marks=team1_marks,
                team2_marks=team2_marks,
                result_summary={
                    'winning_team': winning_team,
                    'cards_played': cards_played,
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
                # Winner gets fun fact from losing team's card
                losing_participants = game.participants.filter(is_winner=False)
                if losing_participants.exists():
                    # Get fun fact from a losing player's card
                    losing_participant = losing_participants.first()
                    if losing_participant.lost_card:
                        # Get explanation from questions associated with the card
                        card_questions = Question.objects.filter(
                            card=losing_participant.lost_card,
                            explanation__isnull=False
                        ).exclude(explanation='')
                        
                        if card_questions.exists():
                            question = card_questions.first()
                            fun_fact = question.explanation
                            
                            # Create response record
                            response, created = GameResponse.objects.get_or_create(
                                game=game,
                                participant=participant,
                                defaults={
                                    'response_type': 'fun_fact',
                                    'fun_fact_text': fun_fact,
                                    'fun_fact_card': losing_participant.lost_card
                                }
                            )
                            
                            responses_data.append({
                                'username': participant.player.username,
                                'player_name': participant.player.player_name,
                                'team': participant.team,
                                'is_winner': True,
                                'response_type': 'fun_fact',
                                'fun_fact': fun_fact,
                                'card': losing_participant.lost_card,
                                'card_info': Question(card=losing_participant.lost_card).get_card_info()
                            })
                        else:
                            responses_data.append({
                                'username': participant.player.username,
                                'player_name': participant.player.player_name,
                                'team': participant.team,
                                'is_winner': True,
                                'response_type': 'fun_fact',
                                'fun_fact': 'Congratulations on winning!',
                                'card': None,
                                'card_info': None
                            })
                    else:
                        responses_data.append({
                            'username': participant.player.username,
                            'player_name': participant.player.player_name,
                            'team': participant.team,
                            'is_winner': True,
                            'response_type': 'fun_fact',
                            'fun_fact': 'Congratulations on winning!',
                            'card': None,
                            'card_info': None
                        })
                else:
                    responses_data.append({
                        'username': participant.player.username,
                        'player_name': participant.player.player_name,
                        'team': participant.team,
                        'is_winner': True,
                        'response_type': 'fun_fact',
                        'fun_fact': 'Congratulations on winning!',
                        'card': None,
                        'card_info': None
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
            'cards_in_play': game.cards_in_play,
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
