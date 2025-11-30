from django.urls import reverse
from rest_framework.test import APITestCase
from portfolio.models import Project, Technology, Skill

class PortfolioAPITests(APITestCase):
    def setUp(self):
        t1 = Technology.objects.create(name='Python')
        p = Project.objects.create(title='P1', slug='p1', description='desc')
        p.technologies.add(t1)
        Skill.objects.create(category='Programming Languages', name='Python')

    def test_projects_list(self):
        url = '/api/v1/projects/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('results' in resp.data)

    def test_contact_submit(self):
        url = '/api/v1/contact/'
        payload = {'name': 'John', 'email': 'john@example.com', 'message': 'Hello'}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_newsletter_subscribe(self):
        url = '/api/v1/newsletter/subscribe/'
        payload = {'email': 'john@example.com'}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)