from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Type
from .serializers import TypeSerializer

# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def view_type(request):
    # GET method to retrieve all types
    if request.method == 'GET':
        type_obj = Type.objects.all()
        serializer = TypeSerializer(type_obj, many=True)
        return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # POST method to create a new type
    elif request.method == 'POST':
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'type created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update a type (full update)
    elif request.method == 'PUT':
        type_obj = Type.objects.get(pk=request.data.get('id'))
        serializer = TypeSerializer(type_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'type updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a type
    elif request.method == 'PATCH':
        type_obj = Type.objects.get(pk=request.data.get('id'))
        serializer = TypeSerializer(type_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'type updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a type
    elif request.method == 'DELETE':
        type_obj = Type.objects.get(pk=request.data.get('id'))
        type_obj.delete()
        return Response({'msg': 'type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)