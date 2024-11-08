from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def view_user(request):
    # GET method to retrieve all users
    if request.method == 'GET':
        user_obj = User.objects.all()
        serializer = UserSerializer(user_obj, many=True)
        return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # POST method to create a new user
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update a User (full update)
    elif request.method == 'PUT':
        user_obj = User.objects.get(pk=request.data.get('id'))
        serializer = UserSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'user updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a user
    elif request.method == 'PATCH':
        user_obj = User.objects.get(pk=request.data.get('id'))
        serializer = UserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'user updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a user
    elif request.method == 'DELETE':
        user_obj = User.objects.get(pk=request.data.get('id'))
        user_obj.delete()
        return Response({'msg': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Lưu người dùng mới vào DB
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            # Trả về token kèm theo thông tin người dùng
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username,
                # Thêm các trường cần thiết từ bảng User
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

