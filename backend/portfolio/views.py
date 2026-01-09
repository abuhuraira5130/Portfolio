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
        
        # Admin Email (Plain text for reliability)
        admin_recipient = settings.CONTACT_RECIPIENT_EMAIL or settings.DEFAULT_FROM_EMAIL
        subject_admin = f"🚀 New Portfolio Inquiry: {data['name']}"
        body_admin = f"New contact form submission:\n\nName: {data['name']}\nEmail: {data['email']}\n\nMessage:\n{data['message']}\n\nSubmitted at: {msg.created_at}"
        
        # Client Email (Polished HTML)
        subject_user = "Thank you for reaching out!"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .container {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px; }}
                .header {{ background: linear-gradient(to right, #6366f1, #a855f7); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                .content {{ padding: 30px; line-height: 1.6; color: #333; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #777; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #6366f1; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                .message-box {{ background-color: #f9fafb; border-left: 4px solid #6366f1; padding: 15px; margin: 20px 0; font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin:0;">Thank You!</h1>
                </div>
                <div class="content">
                    <p>Hi <strong>{data['name']}</strong>,</p>
                    <p>Thanks for reaching out! I've received your message and will get back to you as soon as possible.</p>
                    <div class="message-box">
                        "{data['message']}"
                    </div>
                    <p>In the meantime, feel free to check out more of my work on my portfolio.</p>
                    <a href="https://abu-huraira.vercel.app" class="button">Visit My Portfolio</a>
                </div>
                <div class="footer">
                    <p>&copy; {msg.created_at.year} Abu Huraira. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        emails_sent = 0
        try:
            # Send to admin
            send_mail(subject_admin, body_admin, settings.DEFAULT_FROM_EMAIL, [admin_recipient], fail_silently=False)
            emails_sent += 1
        except Exception as e:
            print(f"Admin email fails: {e}")
            
        try:
            # Send to user (HTML)
            email_user = EmailMessage(
                subject=subject_user,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[data['email']],
            )
            email_user.content_subtype = "html"
            email_user.send(fail_silently=False)
            emails_sent += 1
        except Exception as e:
            print(f"User email fails: {e}")
            
        return Response({'status': 'ok', 'emails_sent': emails_sent}, status=status.HTTP_201_CREATED)

class ResumeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        path = settings.RESUME_FILE
        if not os.path.exists(path):
            raise Http404
        return FileResponse(open(path, 'rb'), content_type='application/pdf')