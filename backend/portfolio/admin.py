from django.contrib import admin
from .models import Project, Technology, Skill, Testimonial, NewsletterSubscription, ContactMessage

class TechnologyInline(admin.TabularInline):
    model = Project.technologies.through
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'featured', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('featured',)
    inlines = [TechnologyInline]
    exclude = ('technologies',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name')
    list_filter = ('category',)
    search_fields = ('name', 'category')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'rating', 'created_at')
    search_fields = ('name', 'company')

@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'confirmed', 'created_at')
    search_fields = ('email',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'handled', 'created_at')
    search_fields = ('name', 'email')