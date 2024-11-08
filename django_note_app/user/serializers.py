from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Tìm kiếm người dùng trong bảng User
        try:
            user = User.objects.filter(username=username, password=password)
            print(user, 'user ne')
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        print(user, 'user ne2')
        # Xác thực người dùng
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        # Nếu xác thực thành công, trả về user
        attrs['user'] = user
        return attrs