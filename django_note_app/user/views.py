from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permission import IsAdminUser  
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# View để xử lý user CRUD
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def view_user(request):
    # GET method to retrieve all users
    if request.method == 'GET':
        # Kiểm tra quyền admin ở đây
        if not request.user.admin:
            return Response({"error": "You do not have permission to view users"}, status=status.HTTP_403_FORBIDDEN)
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

# API đăng ký người dùng mới
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])  # Mã hóa mật khẩu
            user.save()

            # Tạo token xác thực email
            token = RefreshToken.for_user(user).access_token
            verification_link = f"http://127.0.0.1:8000/verify/{str(token)}"

            # Gửi email xác thực
            send_mail(
                subject="Verify your email",
                message=f"Please click the link to verify your email: {verification_link}",
                from_email="your_email@example.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({
                "msg": "User registered successfully. Check your email for the verification link."
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API đăng nhập người dùng
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            # Trả về token kèm theo thông tin người dùng
            return Response(
                {
                    "message": "Login successfully",
                    "data": {
                        "accessToken": str(refresh.access_token),
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "fullname": user.fullname,
                        }
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            # Giải mã token để lấy user_id
            decoded_token = UntypedToken(token)
            user_id = decoded_token.get('user_id')
            
            # Lấy đối tượng người dùng dựa trên user_id
            user = User.objects.get(id=user_id)
            user.status = True  # Cập nhật trạng thái thành đã xác thực
            user.save()

            return HttpResponse("Your email has been verified and your account is now active.", status=200)
        
        except (InvalidToken, TokenError, User.DoesNotExist):
            return HttpResponse("Invalid or expired verification link.", status=400)