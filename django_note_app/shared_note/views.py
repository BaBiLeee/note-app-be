from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SharedNote

@api_view(['GET'])
def shared_note_detail(request, note_id):
    user = request.user
    access_token = request.headers.get("Authorization")  # Giả sử token được gửi qua header

    try:
        # Kiểm tra ghi chú có tồn tại và token chính xác
        shared_note = SharedNote.objects.get(note_id=note_id, shared_with=user, access_token=access_token)
        
        # Kiểm tra quyền truy cập
        note_data = {
            "id": shared_note.note.id,
            "title": shared_note.note.title,
            "content": shared_note.note.content,
            "access_level": shared_note.access_level
        }
        return Response(note_data, status=status.HTTP_200_OK)
        
    except SharedNote.DoesNotExist:
        return Response({"detail": "Access denied or note not found"}, status=status.HTTP_403_FORBIDDEN)
