from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Player
from .serializers import PlayerRegistrationSerializer, PlayerSerializer, PlayerLoginSerializer


@method_decorator(csrf_exempt, name='dispatch')
class PlayerRegistrationView(generics.CreateAPIView):
    """
    API endpoint for player self-registration
    No authentication required
    """
    queryset = Player.objects.all()
    serializer_class = PlayerRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                player = serializer.save()
                
                # Since we're using a custom Player model (not extending User),
                # we'll create a simple token-like response without using DRF's Token model
                # For now, we'll use the player's UUID as a simple token
                response_data = {
                    'message': 'Player registered successfully',
                    'player': PlayerSerializer(player).data,
                    'token': str(player.uuid)  # Using player's UUID as token
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except IntegrityError as e:
                return Response({
                    'error': 'Registration failed',
                    'details': 'Username or email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': 'Registration failed',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Handle validation errors (including duplicate username/email from serializer)
            return Response({
                'error': 'Registration failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def player_login_view(request):
    """
    API endpoint for player login
    No authentication required for this endpoint
    """
    serializer = PlayerLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            # Find player by username
            player = Player.objects.get(username=username)
            
            # Check password
            if check_password(password, player.password):
                # Use player's UUID as token for consistency
                return Response({
                    'message': 'Login successful',
                    'player': PlayerSerializer(player).data,
                    'token': str(player.uuid)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials',
                    'details': 'Username or password is incorrect'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Player.DoesNotExist:
            return Response({
                'error': 'Invalid credentials',
                'details': 'Username or password is incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            'error': 'Invalid input',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def player_logout_view(request):
    """
    API endpoint for player logout
    Requires authentication
    """
    try:
        # Get the token from the request and delete it
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'No token provided'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Token.DoesNotExist:
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Logout failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
def player_profile_view(request):
    """
    API endpoint to get and update player profile
    Requires authentication
    """
    # Get token from Authorization header
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token_key = auth_header.split(' ')[1]
    
    try:
        token = Token.objects.select_related('user').get(key=token_key)
        player = Player.objects.get(id=token.user_id)
        
        if request.method == 'GET':
            return Response(PlayerSerializer(player).data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            serializer = PlayerSerializer(player, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except (Token.DoesNotExist, Player.DoesNotExist):
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'error': 'Profile access failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_age_groups_view(request):
    """
    API endpoint to get available age groups
    No authentication required
    """
    age_groups = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Player.AGE_GROUP_CHOICES
    ]
    
    return Response({
        'age_groups': age_groups
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_provinces_districts_view(request):
    """
    API endpoint to get available provinces and their districts
    No authentication required
    """
    province_districts = {
        'Kigali City': ['Gasabo', 'Kicukiro', 'Nyarugenge'],
        'Northern Province': ['Burera', 'Gakenke', 'Gicumbi', 'Musanze', 'Rulindo'],
        'Southern Province': ['Gisagara', 'Huye', 'Kamonyi', 'Muhanga', 'Nyamagabe', 'Nyanza', 'Nyaruguru', 'Ruhango'],
        'Eastern Province': ['Bugesera', 'Gatsibo', 'Kayonza', 'Kirehe', 'Ngoma', 'Nyagatare', 'Rwamagana'],
        'Western Province': ['Karongi', 'Ngororero', 'Nyabihu', 'Nyamasheke', 'Rubavu', 'Rusizi', 'Rutsiro'],
    }
    
    # Format for frontend consumption
    provinces_data = []
    for province, districts in province_districts.items():
        provinces_data.append({
            'province': province,
            'districts': [{'value': district, 'label': district} for district in districts]
        })
    
    return Response({
        'provinces': provinces_data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gender_choices_view(request):
    """
    API endpoint to get available gender choices
    No authentication required
    """
    genders = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Player.GENDER_CHOICES
    ]
    
    return Response({
        'genders': genders
    }, status=status.HTTP_200_OK)
