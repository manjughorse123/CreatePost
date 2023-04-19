from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAdminUser ,IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import pagination
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db.models import Q

from post.utils import generate_access_token
from .serializers import  *
from .models import *


class LoginView(APIView):
  
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

  
    def post(self, request):

        try:

            username = request.data['username']
            password = request.data['password']
            
            user_obj =authenticate(
                username=username, password=password)
            
            access_token = generate_access_token(user_obj)
            return Response(
                {'success': True,  "token":access_token},
                status=status.HTTP_200_OK)
           

        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': ' Wrong Deail',
                'status': 404, 'is_register': False},
            status=status.HTTP_404_NOT_FOUND)


class CustomPagination(pagination.PageNumberPagination):
    
    page_query_param = "offset"   # this is the "page"
    page_size_query_param="limit" # this is the "page_size"
    page_size = 50
    max_page_size = 100
  
    def get_paginated_response(self, data1):
        return Response({
           
            'post': data1,
           },
        status=status.HTTP_200_OK)
        


class PostListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        
        if request.GET.get("search"):
            postData = Post.objects.filter( Q(body=request.GET["search"]) | Q(title=request.GET["search"]))
            serializer = PostSerializer(postData, many=True)

            postDeta = self.paginate_queryset(serializer.data)
            
            postDeta = self.get_paginated_response(postDeta)
            
            return postDeta
            
        postData = Post.objects.all()
        serializer = PostSerializer(postData, many=True)

        postDeta = self.paginate_queryset(serializer.data)
        
        postDeta = self.get_paginated_response(postDeta)
        
        return postDeta
    
    def post(self, request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                           status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                       status=status.HTTP_400_BAD_REQUEST)


class PostListCreateUpdateAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,pk):
        
        postData = Post.objects.get(id=pk)
        serializer = PostSerializer(postData)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try :
            postData = Post.objects.get(id=pk,author=request.user)
        

            serializer = PostSerializer(postData, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response( {'message':"Data not found!"},status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk, format=None):
        try:
            postData = Post.objects.get(id=pk,author=request.user)
      
            postData.delete()
            return Response({'message':"Post Deleted!"},status=status.HTTP_204_NO_CONTENT)
        except :
            return Response({'message':"Data not found!"}, status=status.HTTP_400_BAD_REQUEST)
    