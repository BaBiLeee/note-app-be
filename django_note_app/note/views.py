from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from shared.models import Shared
from user.models import User
from shared.serializers import SharedSerializer

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])  # Yêu cầu người dùng phải xác thực
def view_note(request):
    if request.method == 'GET':
            if request.user.admin:
                note_obj = Note.objects.all()
            else:
                note_obj = Note.objects.filter(user=request.user.id)

            serializer = NoteSerializer(note_obj, many=True)
            return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # POST method to create a new note
    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'note created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a note
    elif request.method == 'DELETE':
        note_obj = Note.objects.get(pk=request.data.get('id'))
        note_obj.delete()
        return Response({'msg': 'note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Chỉ cho phép người dùng đã đăng nhập
def get_note_by_id(request, note_id):
    try:
        # Lấy đối tượng Note
        note_obj = get_object_or_404(Note, id=note_id)

        # Kiểm tra nếu người dùng là admin
        if request.user.admin:
            serializer = NoteSerializer(note_obj)
            return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        # Kiểm tra nếu người dùng là chủ sở hữu của ghi chú
        if note_obj.user.id == request.user.id:
            serializer = NoteSerializer(note_obj)
            return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        # Kiểm tra nếu ghi chú được chia sẻ với người dùng này
        try:
            share_obj = Shared.objects.get(note=note_obj, shared_user=request.user)
            
            # Kiểm tra quyền xem (VIEW) trong Share model
            if 1:
                serializer = NoteSerializer(note_obj)
                return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        except Shared.DoesNotExist:
            return Response({'msg': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    except Note.DoesNotExist:
        return Response({'msg': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_shared_note(request):
    # Lấy tất cả các đối tượng Shared liên quan đến người dùng
    shared_objects = Shared.objects.filter(shared_user_id=request.user.id)

    # Kiểm tra nếu có ít nhất một đối tượng
    if not shared_objects.exists():
        return Response({'msg': 'No shared notes found'}, status=status.HTTP_404_NOT_FOUND)

    # Chuyển các đối tượng Shared thành dữ liệu qua serializer
    serializer = SharedSerializer(shared_objects, many=True)

    return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Kiểm tra người dùng đã đăng nhập
def share_note(request, note_id):
    try:
        # Lấy thông tin của người dùng và note
        note_obj = Note.objects.get(id=note_id)
        shared_user_id = request.data.get('shared_user_id')  # Gán shared_user_id
        permission = request.data.get('permission')

        # Kiểm tra xem người dùng chia sẻ có phải là chủ sở hữu của note không
        if shared_user_id == request.user.id:
            return Response({'msg': 'User is the owner'}, status=status.HTTP_403_FORBIDDEN)
        
        # Kiểm tra nếu đã chia sẻ note với người dùng này
        shared_objects = Shared.objects.filter(shared_user_id=request.user.id, note_id=note_id)
        shared_objects2 = Shared.objects.filter(shared_user_id=request.user.id, owner=request.user)

        if shared_objects.exists() or shared_objects2.exists():
            return Response({'msg': 'User has already been shared'}, status=status.HTTP_403_FORBIDDEN)
        
        # Kiểm tra quyền SHARE của người dùng
        shared_permission_check = Shared.objects.raw('''
            SELECT * FROM public.shared
            WHERE note_id = %s AND shared_user_id = %s AND (permission & 4) > 0
        ''', [note_obj.id, request.user.id])

        # Kiểm tra quyền của người thực hiện thao tác
        if (note_obj.user.id == request.user.id or request.user.admin) or shared_permission_check:
            # Lấy người dùng được chia sẻ
            shared_user = User.objects.get(id=shared_user_id)

            # Tạo bản ghi Share mới
            Shared.objects.create(
                note=note_obj,
                owner=note_obj.user,
                shared_by=request.user,
                shared_user=shared_user,
                permission=permission
            )
            
            return Response({'msg': 'Note shared successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
    except Note.DoesNotExist:
        return Response({'msg': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Chỉ cho phép người dùng đã đăng nhập
def update_note(request, note_id):
    try:
        # Lấy note theo ID từ request data
        note_obj = Note.objects.get(id=note_id)
        
        # Kiểm tra quyền sở hữu hoặc quyền cập nhật (bitwise permission với giá trị 2)
        shared_permission_check = Shared.objects.raw('''
            SELECT * FROM public.shared
            WHERE note_id = %s AND shared_user_id = %s AND (permission & 2) > 0
        ''', [note_obj.id, request.user.id])

        if request.user.admin or note_obj.user.id == request.user.id or shared_permission_check:
            # Nếu người dùng có quyền, tiến hành cập nhật note
            serializer = NoteSerializer(note_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Note updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Trường hợp người dùng không có quyền cập nhật
            return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    except Note.DoesNotExist:
        return Response({'msg': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Chỉ cho phép người dùng đã đăng nhập
def delete_note(request, note_id):
    try:
        # Lấy note theo ID từ request data
        note_obj = Note.objects.get(id=note_id)
        
        if request.user.admin or note_obj.user.id == request.user.id:
            # Nếu người dùng có quyền, tiến hành cập nhật note
            note_obj.delete()
        return Response({'msg': 'note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Note.DoesNotExist:
        return Response({'msg': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Chỉ cho phép người dùng đã đăng nhập
def change_permission(request):
    try:
        # Lấy note theo ID từ request data
        
        user_id = request.data.get('user_id')
        note_id = request.data.get('note_id')
        shared_obj = Shared.objects.get(note_id=note_id, shared_user_id=user_id)
        
        if request.user.admin or shared_obj.owner_id == request.user.id:
            # Nếu người dùng có quyền, tiến hành cập nhật note
            serializer = SharedSerializer(shared_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Permission updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Trường hợp người dùng không có quyền cập nhật
            return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    except Note.DoesNotExist:
        return Response({'msg': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)