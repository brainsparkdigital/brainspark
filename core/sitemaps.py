from django.contrib.sitemaps import Sitemap
from .models import  Category, Service, Portfolio
from blog.models import BlogPost


from django.contrib.sitemaps import Sitemap


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.publish_date

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Category.objects.all()

class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.all()

class PortfolioSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Portfolio.objects.all()
