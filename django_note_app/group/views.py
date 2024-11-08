from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Group
from .serializers import GroupSerializer

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def view_group(request):
    # GET method to retrieve all groups
    if request.method == 'GET':
        group_obj = Group.objects.all()
        serializer = GroupSerializer(group_obj, many=True)
        return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # POST method to create a new group
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'group created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update a group (full update)
    elif request.method == 'PUT':
        group_obj = Group.objects.get(pk=request.data.get('id'))
        serializer = GroupSerializer(group_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'group updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a group
    elif request.method == 'PATCH':
        group_obj = Group.objects.get(pk=request.data.get('id'))
        serializer = GroupSerializer(group_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'group updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a group
    elif request.method == 'DELETE':
        group_obj = Group.objects.get(pk=request.data.get('id'))
        group_obj.delete()
        return Response({'msg': 'group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)