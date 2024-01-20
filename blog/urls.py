from django.urls import path
 
from .views import BlogPostDetailView, BlogPostListView
 
urlpatterns = [
    path('blog/', BlogPostListView.as_view(), name='blog_list'),
    path('blog/<slug>', BlogPostDetailView.as_view(), name='blog_detail'),
]