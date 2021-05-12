from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, PostUpdateView, PostCreateView, PostDeleteView, like

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create', PostCreateView.as_view(), name='create'),
    path('<slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug>/update/', PostUpdateView.as_view(), name='update'),
    path('<slug>/delete/', PostDeleteView.as_view(), name='delete'),

    path('like/<slug>/', like, name='like'),
]

