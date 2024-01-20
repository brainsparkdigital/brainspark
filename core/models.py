from django.db import models
from django.urls import reverse


class Category(models.Model):
    '''
    Model representing our Core Services (i.e. SEO).
    '''

    # Fields
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(max_length=100, help_text='Write a short description here.')
    icon = models.ImageField(upload_to='media/category_icons/')

    # Meta class to specify verbose names
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # Method to get the absolute URL for a Category instance
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.slug)])

    # Method to represent the Category instance as a string
    def __str__(self):
        return self.name
    

class Service(models.Model):
    '''
    Model representing our Service Names and their details that users can see.
    '''

    # Fields
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_text=models.CharField(max_length=255, blank=True)
    service_text = models.TextField(help_text='Enter your service description here')

    # Method to get the absolute URL for a Service instance
    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.slug)])
    
    # Method to represent the Service instance as a string
    def __str__(self):
        return self.title
    

class PortfolioImage(models.Model):
    '''
    Model representing multiple images for a Portfolio.
    '''

    # Fields
    image = models.ImageField(upload_to='media/portfolio_images/') 

    
class Portfolio(models.Model):
    '''
    Model representing showcasing our works.
    '''

    # Fields
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    text_description = models.TextField(help_text='Enter your project description here')
    images = models.ManyToManyField('PortfolioImage')

    # Method to get the absolute URL for a Portfolio instance
    def get_absolute_url(self):
        return reverse('portfolio_detail', args=[str(self.slug)])
    
    # Method to represent the Portfolio instance as a string
    def __str__(self):
        return self.name


class FAQ(models.Model):
    '''
    Model representing FAQ about a related service.
    '''

    # Fields
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, help_text='Write FAQ Questions.')
    answer = models.TextField(help_text='Write FAQ Answers.')

    # Method to represent the FAQ instance as a string
    def __str__(self):
        return f'Q:{self.question} - A:{self.answer}'


