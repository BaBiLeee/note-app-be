from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import SimpleUserSerializer, UserSerializer, LoginSerializer
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
def user_list(request):
    users = User.objects.all()  # Lấy toàn bộ người dùng
    serializer = SimpleUserSerializer(users, many=True)
    return Response({'message': 'Successfully retrieved user data', 'data': serializer.data}, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def view_user(request):
    if request.method == 'GET':
        if request.user.admin:
            user_obj = User.objects.all()
        else:
            user_obj = User.objects.filter(id=request.user.id)
        
        serializer = UserSerializer(user_obj, many=True)
        return Response({'message': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)
    


    # POST method to create a new user
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update a User (full update)
    elif request.method == 'PUT':
        user_obj = User.objects.get(pk=request.data.get('id'))
        serializer = UserSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a user
    elif request.method == 'PATCH':
        user_obj = User.objects.get(pk=request.data.get('id'))
        serializer = UserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a user
    elif request.method == 'DELETE':
        user_obj = User.objects.get(pk=request.data.get('id'))
        user_obj.delete()
        return Response({'message': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
                "message": "User registered successfully. Check your email for the verification link."
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API đăng nhập người dùng
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Kiểm tra trạng thái tài khoản người dùng
            if not user.status:
                return Response(
                    {"message": "You need to activate your account first"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Tạo token cho người dùng
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
                            "admin": user.admin
                        }
                    }
                },
                status=status.HTTP_200_OK
            )

        # Nếu thông tin đăng nhập không hợp lệ
        return Response(
            {"message": "Invalid login credentials", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            # Decode the token to retrieve the user_id
            decoded_token = UntypedToken(token)
            user_id = decoded_token.get('user_id')

            # Retrieve the user object based on user_id
            user = User.objects.get(id=user_id)
            user.status = True  # Update status to verified
            user.save()

            # HTML response with styling and auto-redirect to login page
            html_content = """
            <html>
                <head>
                    <style>
                        body { 
                            display: flex; 
                            align-items: center; 
                            justify-content: center; 
                            height: 100vh; 
                            background-color: #f3f4f6; 
                            margin: 0; 
                            font-family: Arial, sans-serif; 
                            color: #333; 
                        }
                        .message-box {
                            text-align: center;
                            padding: 20px;
                            border-radius: 8px;
                            background-color: #fff;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            max-width: 400px;
                        }
                        .message-box h2 { 
                            color: #4CAF50; 
                        }
                        .message-box p { 
                            font-size: 16px; 
                        }
                    </style>
                    <script>
                        setTimeout(function(){
                            window.location.href = 'http://localhost:3000/login';
                        }, 2000);
                    </script>
                </head>
                <body>
                    <div class="message-box">
                        <h2>Email Verified</h2>
                        <p>Your email has been verified and your account is now active.</p>
                        <p>You will be redirected to the login page shortly...</p>
                    </div>
                </body>
            </html>
            """

            return HttpResponse(html_content, content_type="text/html", status=200)
        
        except (InvalidToken, TokenError, User.DoesNotExist):
            # Error HTML response
            error_content = """
            <html>
                <head>
                    <style>
                        body { 
                            display: flex; 
                            align-items: center; 
                            justify-content: center; 
                            height: 100vh; 
                            background-color: #f3f4f6; 
                            margin: 0; 
                            font-family: Arial, sans-serif; 
                            color: #333; 
                        }
                        .message-box {
                            text-align: center;
                            padding: 20px;
                            border-radius: 8px;
                            background-color: #fff;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            max-width: 400px;
                        }
                        .message-box h2 { 
                            color: #e74c3c; 
                        }
                        .message-box p { 
                            font-size: 16px; 
                        }
                    </style>
                    <script>
                        setTimeout(function(){
                            window.location.href = 'http://localhost:3000/login';
                        }, 2000);
                    </script>
                </head>
                <body>
                    <div class="message-box">
                        <h2>Verification Failed</h2>
                        <p>Invalid or expired verification link.</p>
                        <p>You will be redirected to the login page shortly...</p>
                    </div>
                </body>
            </html>
            """
            return HttpResponse(error_content, content_type="text/html", status=400)