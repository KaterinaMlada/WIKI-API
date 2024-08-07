from django.urls import reverse
import json
from rest_framework.test import APITestCase

class WikiApiTestCase(APITestCase):

    def test_get_article_success(self):
        response = self.client.get(reverse('get_article', args=['Python']), HTTP_ACCEPT_LANGUAGE='en')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)
    
    def test_search_article(self):
        response = self.client.get('/wiki/some_search/')
        self.assertEqual(response.status_code, 303)
        data = response.json()
        self.assertIn('articles', data)

    def test_article_not_found(self):
        response = self.client.get(reverse('get_article', args=['nonexistentarticle']), HTTP_ACCEPT_LANGUAGE='en')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertNotIn('result', data)
