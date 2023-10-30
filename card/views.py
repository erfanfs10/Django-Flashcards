from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from category.models import Category
from .serializers import CardSerializer
from .models import Card
import json


class CardDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        category_name = request.data.get("category_name", None)
        card_name = request.data.get("card_name", None)

        if category_name is not None and card_name is not None:

            card = get_object_or_404(Card, front=card_name, category__name=category_name,
                                      category__user=request.user)

            serializer = CardSerializer(card)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data={"message": "enter the category_name and card_name!"},
                                 status=status.HTTP_400_BAD_REQUEST)
            

class CardCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        category_name = request.data.get("category_name", None)
        front_name = request.data.get("front_name", None)
        back_name = request.data.get("back_name", None)

        if category_name is not None and front_name is not None and back_name is not None:

            category = get_object_or_404(Category, name=category_name, user=request.user)

            try:
                Card.objects.get(front=front_name, category=category,
                                         category__user=request.user)
                
                return Response(data={"message": f"{front_name} already exist!"},
                             status=status.HTTP_200_OK)
            
            except Card.DoesNotExist:    
                
                with transaction.atomic():
                    Card.objects.create(front=front_name, back=back_name, category=category)

                return Response(data={"message": f"{front_name} create successfully"},
                             status=status.HTTP_200_OK)

        return Response(
            data={"message": "enter the category_name and front_name! and back_name"},
                                 status=status.HTTP_400_BAD_REQUEST)


class CardDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        
        category_name = request.data.get("category_name", None)
        card_name = request.data.get("card_name", None)

        if category_name is not None and card_name is not None:

            card = get_object_or_404(Card, front=card_name, category__name=category_name,
                                      category__user=request.user)
           
            with transaction.atomic():
                card.delete()

            return Response(
                data={"message": f"the {card_name} card deleted from {category_name} category"}
                             ,status=status.HTTP_204_NO_CONTENT)
        
        return Response(data={"message": "enter the category_name and card_name!"},
                                 status=status.HTTP_400_BAD_REQUEST)
    

class CardEdit(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        
        card_edit = request.data.get("card_edit", None)

        if card_edit is not None:

            card_edit = json.loads(card_edit)
            category = get_object_or_404(Category, name=card_edit["category_name"], user=request.user)
            card = get_object_or_404(Card, front=card_edit["old_front"], category=category,
                                      category__user=request.user)
            
            with transaction.atomic():
                card.front = card_edit["new_front"]
                card.back = card_edit["new_back"]
                card.save()

            return Response(data={"message": f"the card edited successfully"}, status=status.HTTP_204_NO_CONTENT)    

        return Response(
            data={"message": 'enter the data with this format {"category_name": "tofel", "old_front":"hello" , "new_front": "new front", "new_back": "new back"}'},
              status=status.HTTP_400_BAD_REQUEST)
    