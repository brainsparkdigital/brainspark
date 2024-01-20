from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from core.models import Category  # Make sure to import your Category model
from django.urls import reverse

from .models import BlogPost  # Adjust the import path based on your project structure

class BlogPostTestCase(TestCase):
    def setUp(self):
        # Create a sample category for testing
        self.category = Category.objects.create(name='Test Category')

    def test_create_blog_post(self):
        # Create a new blog post
        blog_post = BlogPost.objects.create(
            category=self.category,
            title='Test Blog Post',
            text='This is a test blog post.',
            published=True,
        )

        # Check if the blog post was created successfully
        self.assertEqual(blog_post.title, 'Test Blog Post')
        self.assertEqual(blog_post.category, self.category)
        self.assertTrue(blog_post.published)
        self.assertIsNotNone(blog_post.pub_date)

    def test_modify_blog_post(self):
        # Create a blog post
        blog_post = BlogPost.objects.create(
            category=self.category,
            title='Test Blog Post',
            text='This is a test blog post.',
            published=True,
        )

        # Modify the blog post
        blog_post.title = 'Modified Blog Post'
        blog_post.save()

        # Check if the modification was successful
        updated_blog_post = BlogPost.objects.get(pk=blog_post.pk)
        self.assertEqual(updated_blog_post.title, 'Modified Blog Post')

    def test_publish_unpublish_blog_post(self):
        # Create a blog post
        blog_post = BlogPost.objects.create(
            category=self.category,
            title='Test Blog Post',
            text='This is a test blog post.',
            published=False,
        )

        # Publish the blog post
        blog_post.published = True
        blog_post.save()

        # Check if pub_date is set when published
        self.assertIsNotNone(blog_post.pub_date)

        # Unpublish the blog post
        blog_post.published = False
        blog_post.save()

        # Check if pub_date is reset when unpublished
        self.assertIsNone(blog_post.pub_date)

    def test_blog_post_querysets(self):
        # Create published and draft blog posts
        published_post = BlogPost.objects.create(
            category=self.category,
            title='Published Blog Post',
            text='This is a published blog post.',
            published=True,
        )
        draft_post = BlogPost.objects.create(
            category=self.category,
            title='Draft Blog Post',
            text='This is a draft blog post.',
            published=False,
        )

        # Test published queryset
        published_posts = BlogPost.objects.published()
        self.assertIn(published_post, published_posts)
        self.assertNotIn(draft_post, published_posts)

        # Test draft queryset
        draft_posts = BlogPost.objects.draft()
        self.assertIn(draft_post, draft_posts)
        self.assertNotIn(published_post, draft_posts)

    def test_get_absolute_url(self):
        # Create a blog post
        blog_post = BlogPost.objects.create(
            category=self.category,
            title='Test Blog Post',
            text='This is a test blog post.',
            published=True,
        )

        # Test the get_absolute_url method
        expected_url = reverse('blog_detail', kwargs={'slug': blog_post.slug})
        self.assertEqual(blog_post.get_absolute_url(), expected_url)
