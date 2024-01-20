from django.views.generic import ListView, DetailView
from django.views.generic import ListView, DetailView
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.published().order_by('-created')  # Change to '-created' for descending order
    template_name = 'blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 10  # Adjust as needed

class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog_detail.html'
    context_object_name = 'blog_post'
