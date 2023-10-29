from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .serializers import CategoryListSerializer, CardSerializer
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

        name = request.data.get("name", None)
        if name is not None:

            category = get_object_or_404(Category, name=name, user=request.user)
            cards = category.cards.all()
            serializer = CardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(data={"message": "enter the name!"},
                                 status=status.HTTP_400_BAD_REQUEST)


class CategoryAdd(APIView):    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):

        name = request.data.get("name", None)
        if name is not None:

            try:

                Category.objects.get(name=name, user=request.user)
                return Response(data={"message": f"category with name {name} already exist!"},
                                 status=status.HTTP_400_BAD_REQUEST)
            
            except Category.DoesNotExist:

                Category.objects.create(name=name, user=request.user)
                return Response(data={"message": f"category with name {name} created!"},
                                 status=status.HTTP_201_CREATED)    

        return Response(data={"message": "enter the name!"},
                                 status=status.HTTP_400_BAD_REQUEST)
    

class CategoryRename(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        
        name = request.data.get("name", None)
        rename = request.data.get("rename", None)

        if name is not None and rename is not None:

            category = get_object_or_404(Category, name=name, user=request.user)
            category.name = rename
            category.save()

            return Response(data={"message": f"the {name} category name changed to {rename}"},
                             status=status.HTTP_200_OK)
        
        return Response(data={"message": "enter the name and rename!"},
                                 status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDelete(APIView):
    pass    