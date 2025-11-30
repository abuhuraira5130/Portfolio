from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.http import FileResponse, Http404
import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, Technology, Skill, Testimonial, NewsletterSubscription, ContactMessage
from .serializers import (
    ProjectSerializer,
    TechnologySerializer,
    SkillSerializer,
    TestimonialSerializer,
    NewsletterSerializer,
    ContactSerializer,
)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-featured', '-created_at')
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'technologies__name']
    ordering_fields = ['created_at', 'title']
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class SkillListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        skills = Skill.objects.all().order_by('category', 'name')
        grouped = {}
        for s in skills:
            grouped.setdefault(s.category, []).append(s.name)
        return Response(grouped)

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class NewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sub, created = NewsletterSubscription.objects.get_or_create(email=serializer.validated_data['email'])
        if created:
            try:
                send_mail(
                    subject='Subscription Confirmed',
                    message='Thanks for subscribing!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[sub.email],
                    fail_silently=True,
                )
                sub.confirmed = True
                sub.save()
            except Exception:
                pass
        return Response({'email': sub.email, 'confirmed': sub.confirmed}, status=status.HTTP_201_CREATED)

class ContactSubmitView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        msg = serializer.save()
        
        # Send email to admin
        admin_recipient = settings.CONTACT_RECIPIENT_EMAIL or settings.DEFAULT_FROM_EMAIL
        subject_admin = f"New Contact Form Submission: {data['name']}"
        body_admin = f"""
New contact form submission:

Name: {data['name']}
Email: {data['email']}
Message:
{data['message']}

Submitted at: {msg.created_at}
"""
        
        # Send email to user
        subject_user = "Thank you for contacting us!"
        body_user = f"""
Hi {data['name']},

Thank you for reaching out! We have received your message and will get back to you shortly.

Best regards,
Portfolio Team
"""
        
        # Send both emails with proper error handling
        emails_sent = 0
        
        try:
            # Send to admin
            send_mail(
                subject=subject_admin,
                message=body_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_recipient],
                fail_silently=False,
            )
            emails_sent += 1
        except Exception as e:
            print(f"Failed to send admin email: {e}")
        
        try:
            # Send to user
            send_mail(
                subject=subject_user,
                message=body_user,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[data['email']],
                fail_silently=False,
            )
            emails_sent += 1
        except Exception as e:
            print(f"Failed to send user email: {e}")
        
        return Response({
            'status': 'ok', 
            'message': 'Form submitted successfully',
            'emails_sent': emails_sent
        }, status=status.HTTP_201_CREATED)

class ResumeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        path = settings.RESUME_FILE
        if not os.path.exists(path):
            raise Http404
        return FileResponse(open(path, 'rb'), content_type='application/pdf')