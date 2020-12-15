from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareserverapi.models import Category
from rareserverapi.serializers import CategorySerializer


class CategoriesViewSet(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):

        categories = Category.objects.all().order_by("label")

        serializer = CategorySerializer(
          categories, many=True, context={'request': request})
        return Response(serializer.data)

    
    def create(self, request):

        category = Category()
        category.label = request.data["label"]

        try:
          category.save()
          serializer = CategorySerializer(category, context={'request': request})
          return Response(serializer.data)

        except ValidationError as ex:
          return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):

        try:
          category = Category.objects.get(pk=pk)
          category.delete()

          return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):

        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]

        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
