from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Service, Portfolio, FAQ
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from blog.models import BlogPost
from .forms import MeetingForm, ContactForm
from django.views.decorators.http import require_http_methods
from django.views import View

class HomePageView(TemplateView):
    """
    View for rendering the home page.

    Attributes:
        template_name (str): The template to render for the home page.
    """

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Retrieve context data for rendering the home page.

        Returns:
            dict: Context data containing categories, portfolios, and latest blog posts.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['portfolios'] = Portfolio.objects.all()
        context['latest_blog_posts'] = BlogPost.objects.published().order_by('-pub_date')[:3]
        return context

class AboutView(View):
    """
    View for rendering the about page.

    Attributes:
        template_name (str): The template to render for the about page.
    """

    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the about page.

        Returns:
            HttpResponse: Rendered about page template.
        """
        return render(request, self.template_name)

@require_http_methods(["GET"])
def robots_txt(request):
    """
    View for serving robots.txt content.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Response containing robots.txt content.
    """
    return HttpResponse(robots_txt_content, content_type="text/plain")

robots_txt_content = """\
User-Agent: *
Disallow: /private/
Disallow: /junk/

User-agent: GPTBot
Disallow: /
"""

class CategoryListView(ListView):
    """
    View for listing categories.

    Attributes:
        model: The model to use for listing categories.
        template_name (str): The template to render for the category list.
        context_object_name (str): The variable name for the list of categories in the template.
    """

    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    """
    View for displaying details of a category.

    Attributes:
        model: The model to use for retrieving category details.
        template_name (str): The template to render for the category details.
        context_object_name (str): The variable name for the category details in the template.
    """

    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        """
        Retrieve context data for rendering the category details page.

        Returns:
            dict: Context data containing category details and related services.
        """
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(category=self.object)
        return context

class ServiceListView(ListView):
    """
    View for listing services.

    Attributes:
        model: The model to use for listing services.
        template_name (str): The template to render for the service list.
        context_object_name (str): The variable name for the list of services in the template.
    """

    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        """
        Get the queryset for listing services based on the selected category slug.

        Returns:
            QuerySet: Filtered services based on the selected category.
        """
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Service.objects.filter(category=category)

class ServiceDetailView(DetailView):
    """
    View for displaying details of a service.

    Attributes:
        model: The model to use for retrieving service details.
        template_name (str): The template to render for the service details.
        context_object_name (str): The variable name for the service details in the template.
    """

    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

class PortfolioListView(ListView):
    """
    View for listing portfolios.

    Attributes:
        model: The model to use for listing portfolios.
        template_name (str): The template to render for the portfolio list.
        context_object_name (str): The variable name for the list of portfolios in the template.
    """

    model = Portfolio
    template_name = 'portfolio_list.html'
    context_object_name = 'portfolios'

class PortfolioDetailView(DetailView):
    """
    View for displaying details of a portfolio.

    Attributes:
        model: The model to use for retrieving portfolio details.
        template_name (str): The template to render for the portfolio details.
        context_object_name (str): The variable name for the portfolio details in the template.
    """

    model = Portfolio
    template_name = 'portfolio_detail.html'
    context_object_name = 'portfolio'

class FAQDetailView(DetailView):
    """
    View for displaying details of an FAQ.

    Attributes:
        model: The model to use for retrieving FAQ details.
        template_name (str): The template to render for the FAQ details.
        context_object_name (str): The variable name for the FAQ details in the template.
    """

    model = FAQ
    template_name = 'faq_detail.html'
    context_object_name = 'faq'

class SuccessView(View):
    """
    View for displaying the success page.

    Attributes:
        template_name (str): The template to render for the success page.
    """

    template_name = 'success.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the success page.

        Returns:
            HttpResponse: Rendered success page template.
        """
        return render(request, self.template_name)

def book_meeting(request):
    """
    View for handling the booking of a meeting.

    If the request method is POST and the form is valid,
    store the meeting data in the session and redirect to the contact form.
    Otherwise, render the book meeting form.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered book meeting form or redirect to contact form.
    """
    if request.method == 'POST':
        meeting_form = MeetingForm(request.POST)
        if meeting_form.is_valid():
            meeting_data = {
                'date': meeting_form.cleaned_data['date'].isoformat(),
                'time': meeting_form.cleaned_data['time'].isoformat(),
            }
            request.session['meeting_data'] = meeting_data
            return redirect('contact')
    else:
        meeting_form = MeetingForm()

    return render(request, 'book_meeting.html', {'form': meeting_form})

def contact(request):
    """
    View for handling the contact form submission.

    If the request method is POST and the form is valid,
    send an email with the contact form data.
    If there is meeting data in the session, send a combined email.
    Clear the session data after processing and render the success page.
    Otherwise, render the contact form.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered success page or contact form template.
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            meeting_data = request.session.get('meeting_data', None)

            if meeting_data:
                send_combined_email(contact_form.cleaned_data, meeting_data)
            else:
                send_email(contact_form.cleaned_data)

            request.session.pop('meeting_data', None)

            return render(request, 'success.html')
    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'form': contact_form})

def send_email(data):
    """
    Send an email with contact form data.

    Args:
        data (dict): Dictionary containing contact form data.
    """
    send_mail(
        subject=f'Subject: New Contact Form Submission',
        message=f'Name: {data["name"]}\nEmail: {data["email"]}\nPhone: {data["phone_number"]}\n'
                f'Address: {data["address"]}\nService Interest: {data["service_interest"]}\n'
                f'How Found Us: {data["how_found_us"]}\nMessage: {data["message"]}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['zahidhasan2597@gmail.com', 'zahidhasan9297@gmail.com'],
        fail_silently=False,
    )

def send_combined_email(contact_data, meeting_data):
    """
    Send a combined email with contact and meeting form data.

    Args:
        contact_data (dict): Dictionary containing contact form data.
        meeting_data (dict): Dictionary containing meeting form data.
    """
    send_mail(
        subject=f'Subject: New Meeting Form Submission',
        message=f'Meeting Date: {meeting_data["date"]}\nMeeting Time: {meeting_data["time"]}\n\n'
                f'\nName: {contact_data["name"]}\nEmail: {contact_data["email"]}\n'
                f'Phone: {contact_data["phone_number"]}\nService: {contact_data["service_interest"]}\n'
                f'How Found us: {contact_data["how_found_us"]}\nMessage: {contact_data["message"]}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['zahidhasan2597@gmail.com', 'zahidhasan9297@gmail.com'],
        fail_silently=False,
    )
