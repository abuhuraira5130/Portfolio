from django.core.management.base import BaseCommand
from portfolio.models import Technology, Project, Skill, Testimonial

class Command(BaseCommand):
    help = 'Seed portfolio data'

    def handle(self, *args, **options):
        py, _ = Technology.objects.get_or_create(name='Python')
        dj, _ = Technology.objects.get_or_create(name='Django')
        nx, _ = Technology.objects.get_or_create(name='Next.js')

        p1, _ = Project.objects.get_or_create(
            title='AI Agent Framework', slug='ai-agent-framework',
            description='Autonomous AI agent system using Python and LLM APIs.',
            link='https://github.com/yourusername/ai-agent-framework',
            github='https://github.com/yourusername/ai-agent-framework',
            image='/ai-agent-dashboard-with-neural-network-visualizati.jpg',
            featured=True,
        )
        p1.technologies.set([py])

        p2, _ = Project.objects.get_or_create(
            title='Django REST API Backend', slug='django-rest-api-backend',
            description='Scalable REST API backend using Django and MySQL.',
            link='https://api.example.com/docs',
            github='https://github.com/yourusername/django-api',
            image='/backend-api-architecture-diagram.jpg',
            featured=False,
        )
        p2.technologies.set([dj])

        Skill.objects.get_or_create(category='Programming Languages', name='Python')
        Skill.objects.get_or_create(category='Frontend & UI', name='Next.js')
        Skill.objects.get_or_create(category='Backend & Frameworks', name='Django')

        Testimonial.objects.get_or_create(
            name='Jane Doe', role='CTO', company='TechCorp',
            content='Great collaboration and high-quality delivery.', rating=5,
        )
        self.stdout.write(self.style.SUCCESS('Portfolio seed data inserted'))