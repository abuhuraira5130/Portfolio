from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    TechnologyViewSet,
    SkillListView,
    TestimonialViewSet,
    NewsletterSubscribeView,
    ContactSubmitView,
    ResumeView,
)

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('technologies', TechnologyViewSet, basename='technology')
router.register('testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),
    path('skills/', SkillListView.as_view(), name='skills-list'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('contact/', ContactSubmitView.as_view(), name='contact-submit'),
    path('resume/', ResumeView.as_view(), name='resume-view'),
]