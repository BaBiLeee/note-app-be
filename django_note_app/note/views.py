from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
# Create your views here.

# class NoteViewSet(viewsets.ModelViewSet):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

# class TypeViewSet(viewsets.ModelViewSet):
#     queryset = Type.objects.all()
#     serializer_class = TypeSerializer

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# @api_view()
# def view_dtl(request):
#     return Response({'success': 409, 'message': 'api'})


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def view_note(request):
    # GET method to retrieve all notes
    if request.method == 'GET':
        note_obj = Note.objects.all()
        serializer = NoteSerializer(note_obj, many=True)
        return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # POST method to create a new note
    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'note created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update a note (full update)
    elif request.method == 'PUT':
        note_obj = Note.objects.get(pk=request.data.get('id'))
        serializer = NoteSerializer(note_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'note updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a note
    elif request.method == 'PATCH':
        note_obj = Note.objects.get(pk=request.data.get('id'))
        serializer = NoteSerializer(note_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'note updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a note
    elif request.method == 'DELETE':
        note_obj = Note.objects.get(pk=request.data.get('id'))
        note_obj.delete()
        return Response({'msg': 'note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)