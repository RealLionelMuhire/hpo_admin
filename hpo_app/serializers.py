from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Player


class PlayerRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for player self-registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Player
        fields = [
            'player_name', 'username', 'email', 'phone', 'password', 'password_confirm',
            'age_group', 'gender', 'province', 'district'
        ]
        extra_kwargs = {
            'player_name': {'required': True},
            'username': {'required': True},
            'phone': {'required': True},
            'email': {'required': False},
            'age_group': {'required': False},
            'gender': {'required': False},
            'province': {'required': False},
            'district': {'required': False},
        }
    
    def validate(self, attrs):
        """Validate password confirmation and other fields"""
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Remove password_confirm from attrs as it's not a model field
        attrs.pop('password_confirm', None)
        
        # Validate province-district combination if both are provided
        province = attrs.get('province')
        district = attrs.get('district')
        
        if province and district:
            # Province-district mapping
            province_districts = {
                'Kigali City': ['Gasabo', 'Kicukiro', 'Nyarugenge'],
                'Northern Province': ['Burera', 'Gakenke', 'Gicumbi', 'Musanze', 'Rulindo'],
                'Southern Province': ['Gisagara', 'Huye', 'Kamonyi', 'Muhanga', 'Nyamagabe', 'Nyanza', 'Nyaruguru', 'Ruhango'],
                'Eastern Province': ['Bugesera', 'Gatsibo', 'Kayonza', 'Kirehe', 'Ngoma', 'Nyagatare', 'Rwamagana'],
                'Western Province': ['Karongi', 'Ngororero', 'Nyabihu', 'Nyamasheke', 'Rubavu', 'Rusizi', 'Rutsiro'],
            }
            
            valid_districts = province_districts.get(province, [])
            if district not in valid_districts:
                raise serializers.ValidationError(f"District '{district}' is not valid for '{province}' province.")
        
        return attrs
    
    def validate_username(self, value):
        """Validate username uniqueness"""
        if Player.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_email(self, value):
        """Validate email uniqueness if provided"""
        if value and Player.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validated_data):
        """Create new player with hashed password"""
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])
        
        # Create the player
        player = Player.objects.create(**validated_data)
        return player


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for general Player data (without sensitive fields)"""
    
    class Meta:
        model = Player
        fields = [
            'id', 'player_name', 'username', 'email', 'phone',
            'age_group', 'gender', 'province', 'district',
            'points', 'games_played', 'games_won', 'win_rate',
            'created_at'
        ]
        read_only_fields = ['id', 'points', 'games_played', 'games_won', 'win_rate', 'created_at']


class PlayerLoginSerializer(serializers.Serializer):
    """Serializer for player login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
