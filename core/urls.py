# core/urls.py

from django.urls import path, re_path
from django.shortcuts import redirect
from . import views

urlpatterns = [

    # 🔁 Root Redirect to Feed
    path('', lambda request: redirect('feed'), name='root_redirect'),

    # 🔐 Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 📰 Feed
    path('feed/', views.feed, name='feed'),
    path('following/', views.following_feed, name='following_feed'),
    path('explore/', views.explore, name='explore'),

    # 📝 Posts
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.like, name='like'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),

    # 💬 Comments
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # 👤 User Profiles
    path('profile/change-username/', views.change_username, name='change_username'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),

    # 👥 Guest Profile
    path('guest/profile/<str:username>/', views.guest_profile, name='guest_profile'),

    # 🔍 Search
    path('search/', views.search_users, name='search_users'),

    # 🏷 Hashtags
    path('hashtag/<str:tag>/', views.hashtag_view, name='hashtag_posts'),

    # 🔔 Notifications
    path('notifications/', views.notifications_view, name='notifications'),
]
