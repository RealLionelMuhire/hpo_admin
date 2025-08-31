from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Player
import uuid


class PlayerTokenAuthentication(BaseAuthentication):
    """
    Custom token authentication using Player UUID as token
    """
    keyword = 'Token'
    
    def authenticate(self, request):
        auth = self.get_authorization_header(request).split()
        
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, key):
        try:
            # Validate that the token is a valid UUID
            uuid.UUID(key)
            # Find player by UUID
            player = Player.objects.get(uuid=key)
        except (ValueError, Player.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        return (player, key)
    
    def get_authorization_header(self, request):
        """
        Return request's 'Authorization:' header, as a bytestring.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            auth = auth.encode('iso-8859-1')
        return auth
