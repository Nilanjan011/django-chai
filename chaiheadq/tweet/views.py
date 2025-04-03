from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, LoginForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

def tweet_create(request):
    if request.method == 'POST':
        
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            print('request.user ===============', request)
            tweet = form.save(commit=False) # commit=False means we don't save data in to our database only in memory
            tweet.user = request.user
            tweet.save()

            return redirect('tweet_list')
        else:
            return "form is not valid"
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('tweet_list')
        else:
            return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet})
    else:
        form = TweetForm(instance=tweet)
        return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet})


def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    tweet.delete()
    return redirect('tweet_list')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirect if already logged in

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('index')  # Redirect to homepage
            else:
                messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page