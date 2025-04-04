from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.Login.as_view()),
   path('tweet/', views.TweetList.as_view()),
   path('tweet/<int:pk>', views.TweetDetail.as_view(), name='tweet_detail'),

]
