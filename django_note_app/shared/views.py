# shared/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Shared
from .serializers import SharedSerializer
from note.models import Note
from rest_framework.exceptions import PermissionDenied, NotFound

class SharedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Lấy danh sách ghi chú mà người dùng hiện tại được chia sẻ
    def list(self, request):
        shared_notes = Shared.objects.filter(shared=request.user, can_view=True)
        serializer = SharedSerializer(shared_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Lấy chi tiết một ghi chú được chia sẻ nếu có quyền xem
    def retrieve(self, request, pk=None):
        try:
            shared_note = Shared.objects.get(note_id=pk, shared=request.user, can_view=True)
            serializer = SharedSerializer(shared_note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Shared.DoesNotExist:
            raise NotFound("Ghi chú này không tồn tại hoặc bạn không có quyền truy cập.")

    # Tạo bản ghi chia sẻ mới
    def create(self, request):
        serializer = SharedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Cập nhật quyền chia sẻ của ghi chú
    def update(self, request, pk=None):
        try:
            shared_note = Shared.objects.get(note_id=pk, shared=request.user, can_edit=True)
            print("hehe", request.user)
            serializer = SharedSerializer(shared_note, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Shared.DoesNotExist:
            raise PermissionDenied("Bạn không có quyền sửa ghi chú này.")
