from django.urls import reverse  # Import the reverse function from Django
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Service, Portfolio, PortfolioImage, FAQ

class CategoryTestCase(TestCase):
    """
    Test case for the Category model.
    """
    def test_get_absolute_url(self):
        """
        Test the get_absolute_url method of the Category model.
        """
        # Create a Category instance for testing
        category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            short_description='Short description for testing.',
            icon=SimpleUploadedFile("icon.jpg", b"file_content", content_type="image/jpeg"),
        )
        # Generate the expected URL using reverse
        expected_url = reverse('category_detail', args=[str(category.slug)])
        # Check if the generated URL matches the expected URL
        self.assertEqual(category.get_absolute_url(), expected_url)

    def test_category_str_method(self):
        """
        Test the __str__ method of the Category model.
        """
        # Create a Category instance for testing
        category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            short_description='Short description for testing.',
            icon=SimpleUploadedFile("icon.jpg", b"file_content", content_type="image/jpeg"),
        )
        # Check if the string representation of the category matches the expected value
        self.assertEqual(str(category), 'Test Category')

class ServiceTestCase(TestCase):
    """
    Test case for the Service model.
    """
    def setUp(self):
        # Create a Category instance for testing
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            short_description='Short description for testing.',
            icon=SimpleUploadedFile("icon.jpg", b"file_content", content_type="image/jpeg"),
        )

    def test_get_absolute_url(self):
        """
        Test the get_absolute_url method of the Service model.
        """
        # Create a Service instance for testing
        service = Service.objects.create(
            category=self.category,
            title='Test Service',
            slug='test-service',
            short_text='Short text for testing.',
            service_text='Service description for testing.',
        )
        # Generate the expected URL using reverse
        expected_url = reverse('service_detail', args=[str(service.slug)])
        # Check if the generated URL matches the expected URL
        self.assertEqual(service.get_absolute_url(), expected_url)

    def test_service_str_method(self):
        """
        Test the __str__ method of the Service model.
        """
        # Create a Service instance for testing
        service = Service.objects.create(
            category=self.category,
            title='Test Service',
            slug='test-service',
            short_text='Short text for testing.',
            service_text='Service description for testing.',
        )
        # Check if the string representation of the service matches the expected value
        self.assertEqual(str(service), 'Test Service')

class PortfolioTestCase(TestCase):
    """
    Test case for the Portfolio model.
    """
    def setUp(self):
        # Create a Category instance for testing
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            short_description='Short description for testing.',
            icon=SimpleUploadedFile("icon.jpg", b"file_content", content_type="image/jpeg"),
        )

    def test_get_absolute_url(self):
        """
        Test the get_absolute_url method of the Portfolio model.
        """
        # Create a Portfolio instance for testing
        portfolio = Portfolio.objects.create(
            category=self.category,
            name='Test Portfolio',
            slug='test-portfolio',
            text_description='Portfolio description for testing.',
        )
        # Generate the expected URL using reverse
        expected_url = reverse('portfolio_detail', args=[str(portfolio.slug)])
        # Check if the generated URL matches the expected URL
        self.assertEqual(portfolio.get_absolute_url(), expected_url)

    def test_portfolio_str_method(self):
        """
        Test the __str__ method of the Portfolio model.
        """
        # Create a Portfolio instance for testing
        portfolio = Portfolio.objects.create(
            category=self.category,
            name='Test Portfolio',
            slug='test-portfolio',
            text_description='Portfolio description for testing.',
        )
        # Check if the string representation of the portfolio matches the expected value
        self.assertEqual(str(portfolio), 'Test Portfolio')

class FAQTestCase(TestCase):
    """
    Test case for the FAQ model.
    """
    def setUp(self):
        # Create a Category instance for testing
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            short_description='Short description for testing.',
            icon=SimpleUploadedFile("icon.jpg", b"file_content", content_type="image/jpeg"),
        )
        # Create a Service instance for testing
        self.service = Service.objects.create(
            category=self.category,
            title='Test Service',
            slug='test-service',
            short_text='Short text for testing.',
            service_text='Service description for testing.',
        )

    def test_faq_str_method(self):
        """
        Test the __str__ method of the FAQ model.
        """
        # Create an FAQ instance for testing
        faq = FAQ.objects.create(
            service=self.service,
            question='Test Question',
            answer='Test Answer',
        )
        # Generate the expected string representation
        expected_str = f'Q:{faq.question} - A:{faq.answer}'
        # Check if the generated string representation matches the expected value
        self.assertEqual(str(faq), expected_str)
