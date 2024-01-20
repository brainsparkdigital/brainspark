from django.urls import path
from .views import (
    AboutView, CategoryListView, CategoryDetailView,
    ServiceListView, ServiceDetailView,
    PortfolioListView, PortfolioDetailView,
    FAQDetailView, HomePageView, SuccessView,
    contact, book_meeting
)
from core.views import robots_txt
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogPostSitemap, CategorySitemap, ServiceSitemap, PortfolioSitemap

# Sitemaps configuration
sitemaps = {
    'blogposts': BlogPostSitemap,
    'categories': CategorySitemap,
    'services': ServiceSitemap,
    'portfolios': PortfolioSitemap,
}

urlpatterns = [
    # Home Page
    path('', HomePageView.as_view(), name='home'),

    # Robots.txt for search engine crawlers
    path("robots.txt/", robots_txt),

    # Sitemap XML for search engines
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # About Page
    path('about/', AboutView.as_view(), name='about'),

    # Category List
    path('our-services/', CategoryListView.as_view(), name='category_list'),

    # Category Detail
    path('our-services/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    # Service List
    path('our-services/<slug:slug>/services/', ServiceListView.as_view(), name='service_list'),

    # Service Detail
    path('our-services/services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),

    # Portfolio List
    path('portfolio/', PortfolioListView.as_view(), name='portfolio_list'),

    # Portfolio Detail
    path('portfolio/<slug:slug>/', PortfolioDetailView.as_view(), name='portfolio_detail'),

    # FAQ Detail
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq_detail'),

    # Contact Page
    path('contact/', contact, name='contact'),

    # Success Page
    path('success/', SuccessView.as_view(), name='success'),

    # Book Meeting Page
    path('book-meeting/', book_meeting, name='book_meeting'),
]

