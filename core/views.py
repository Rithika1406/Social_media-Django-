# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm, UsernameChangeForm
from .utils import create_notification, parse_tags_and_mentions
from .utils import get_trending_hashtags

import re



# Signup View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View 
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Feed View (with tag/mention parsing)
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.parsed_content = parse_tags_and_mentions(post.content)
    if request.user.is_authenticated:
        return render(request, 'feed.html', {'posts': posts})
    else:
        return render(request, 'guest_feed.html', {'posts': posts})

# Create Post View
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Mention Notification Logic
            mentioned_users = re.findall(r'@(\w+)', post.content)
            for username in mentioned_users:
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user != request.user:
                        create_notification(
                            recipient=mentioned_user,
                            message=f"You were mentioned in a post by {request.user.username}.",
                            link=f"/profile/{request.user.username}/"
                        )
                except User.DoesNotExist:
                    pass

            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

# Delete Post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    return redirect('feed')

# Create Comment
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            if post.user != request.user:
                create_notification(
                    recipient=post.user,
                    message=f"{request.user.username} commented on your post.",
                    link=f"/profile/{request.user.username}/"
                )
            return redirect('feed')
    else:
        form = CommentForm()
    return render(request, 'comment_create.html', {'form': form, 'post': post})

# Delete Comment
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    comment.delete()
    return redirect('feed')

# Like Post
@login_required
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like_obj.delete()
    else:
        if post.user != request.user:
            create_notification(
                recipient=post.user,
                message=f"{request.user.username} liked your post.",
                link=f"/profile/{request.user.username}/"
            )
    return redirect('feed')

# User Profile View
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    likes = Like.objects.filter(user=user)

    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    context = {
        'profile_user': user,
        'posts': posts,
        'likes': likes,
        'is_following': is_following
    }
    return render(request, 'user_profile.html', context)

# Guest Profile View
def guest_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'guest_profile.html', {'profile_user': user, 'posts': posts})

# Change Username
@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your username has been updated.')
            return redirect('user_profile', user.username)
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'change_username.html', {'form': form})

# Search Users
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )
    return render(request, 'search_users.html', {'users': users, 'query': query})

# Toggle Follow
@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('user_profile', username=username)

    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow_obj.delete()
        messages.info(request, f"You unfollowed {target_user.username}")
    else:
        create_notification(
            recipient=target_user,
            message=f"{request.user.username} started following you.",
            link=f"/profile/{request.user.username}/"
        )
        messages.success(request, f"You followed {target_user.username}")

    return redirect('user_profile', username=username)

# Following Feed
@login_required
def following_feed(request):
    followed_users = request.user.following.values_list('following', flat=True)
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
    for post in posts:
        post.parsed_content = parse_tags_and_mentions(post.content)
    return render(request, 'following_feed.html', {'posts': posts})

# Hashtag Feed
def hashtag_view(request, tag):
    posts = Post.objects.filter(content__icontains=f'#{tag}')
    for post in posts:
        post.parsed_content = parse_tags_and_mentions(post.content)
    return render(request, 'hashtag_posts.html', {'tag': tag, 'posts': posts})

# Notifications View
@login_required
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


def explore(request):
    posts = Post.objects.all().order_by('-created_at')[:50]  # Recent 50 posts
    trending_tags = get_trending_hashtags()
    return render(request, 'explore.html', {
        'posts': posts,
        'trending_tags': trending_tags
    })

def hashtag_view(request, tag):
    posts = Post.objects.filter(content__icontains=f'#{tag}')
    for post in posts:
        post.parsed_content = parse_tags_and_mentions(post.content)
    return render(request, 'hashtag_posts.html', {'tag': tag, 'posts': posts})
