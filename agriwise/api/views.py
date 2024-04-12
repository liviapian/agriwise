from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView, status
from rest_framework.response import Response
from app.models import List, Item
from .serializers import ListSerializer, ListDetailSerializer


class ListTODOS(APIView):
    """List all TODO lists."""

    def get(self, request):
        lists = List.objects.filter(user=request.user)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DetailTODOS(APIView):
    '''Details a TODO list.'''

    def get(self, request, list_id):
        list = get_object_or_404(List, pk=list_id, user=request.user)
        serializer = ListDetailSerializer(list, many=False)
        return Response(serializer.data)

    def delete(self, request, list_id):
        list = get_object_or_404(List, pk=list_id, user=request.user)
        list.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def put(self, request, list_id):
        list = get_object_or_404(List, pk=list_id, user=request.user)
        serializer = ListDetailSerializer(list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)