from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'avatar', 'phone', 'date_of_birth', 'address',
            'city', 'state', 'country', 'zip_code', 'is_verified'
        ]
        read_only_fields = ['id', 'is_verified']

class UserDetailSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['created_at', 'updated_at']
