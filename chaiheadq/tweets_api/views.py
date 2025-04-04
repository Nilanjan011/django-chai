import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TweetSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from tweet.models import Tweet
from rest_framework.parsers import MultiPartParser, FormParser

class TweetList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        tweets = TweetSerializer(Tweet.objects.all().order_by('-id'), many=True, context={'request': request})
        return Response(tweets.data)

    def post(self, request,  *args, **kwargs):
        serializer = TweetSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TweetDetail(APIView):  # Use this for individual tweet deletion
    def delete(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)

            # Store image path before deleting the object
            if tweet.photo and os.path.isfile(tweet.photo.path):
                os.remove(tweet.photo.path)  # Delete the image file

            tweet.delete()  # Delete the Tweet instance

            return Response({"message": "Tweet and image deleted."}, status=status.HTTP_204_NO_CONTENT)

        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found."}, status=status.HTTP_404_NOT_FOUND)




class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.get(email=email)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.user.is_authenticated:
            print(request.user.username , request.user.email, request.user.id)
            return Response({'message': 'You are logged in'}, status=status.HTTP_200_OK)
        return Response({'message': 'You are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    
