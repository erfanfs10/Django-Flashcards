from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from card.serializers import CardSerializer
from .serializers import CategoryListSerializer
from .models import Category


class CategoryList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        categories = Category.objects.filter(user=self.request.user).defer("user")
        return categories
    

class CategoryDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        category_name = request.data.get("category_name", None)
        if category_name is not None:

            category = get_object_or_404(Category, name=category_name, user=request.user)
            cards = category.cards.all().defer("category").order_by("-created")
        
            serializer = CardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(data={"message": "enter the category_name!"},
                                 status=status.HTTP_400_BAD_REQUEST)


class CategoryAdd(APIView):    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):

        category_name = request.data.get("category_name", None)
        if category_name is not None:

            try:

                Category.objects.get(name=category_name, user=request.user)
                return Response(data={"message": f"category with name {category_name}\
                                       already exist!"},
                                 status=status.HTTP_400_BAD_REQUEST)
            
            except Category.DoesNotExist:

                with transaction.atomic():
                    Category.objects.create(name=category_name, user=request.user)

                return Response(
                    data={"message": f"category with name {category_name} created!"},
                      status=status.HTTP_201_CREATED)    

        return Response(data={"message": "enter the category_name!"},
                                 status=status.HTTP_400_BAD_REQUEST)
    

class CategoryRename(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        
        category_name = request.data.get("category_name", None)
        category_rename = request.data.get("category_rename", None)

        if category_name is not None and category_rename is not None:

            category = get_object_or_404(Category, name=category_name, user=request.user)

            with transaction.atomic():
                category.name = category_rename
                category.save()

            return Response(
                data={"message": f"the {category_name} category name changed to {category_rename}"}
                , status=status.HTTP_200_OK)
        
        return Response(data={"message": "enter the category_name and category_rename!"},
                                 status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):

        category_name = request.data.get("category_name", None)

        if category_name is not None:

            category = get_object_or_404(Category, name=category_name, user=request.user)
            
            with transaction.atomic():
                category.delete()

            return Response(data={"message": f"the {category_name} category deleted!"},
                             status=status.HTTP_200_OK)
        
        return Response(data={"message": "enter the category_name!"},
                                 status=status.HTTP_400_BAD_REQUEST)
    