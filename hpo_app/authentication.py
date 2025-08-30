from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from .models import Player


class PlayerTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication for Player model
    """
    model = Token
    
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        # Instead of getting the User, get the Player by the token's user_id
        try:
            player = Player.objects.get(id=token.user_id)
        except Player.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        if not player:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        
        return (player, token)
