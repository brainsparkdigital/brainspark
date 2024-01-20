from django.contrib import admin
from .models import Category, FAQ, Portfolio, PortfolioImage, Service

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

class FAQInline(admin.TabularInline):
    model = FAQ

# class PortfolioImageInline(admin.TabularInline):
#     model = PortfolioImage

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    inlines = [FAQInline]

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    # inlines = [PortfolioImageInline]


admin.site.register(Category)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(PortfolioImage)
admin.site.register(FAQ)
