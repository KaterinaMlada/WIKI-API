"""
Modul obsahuje testy pro API koncové body wiki aplikace.

Importované knihovny:
- 'json': Používá se pro serializaci a deserializaci JSON dat v testovacích metodách.
- 'django.urls.reverse': Používá se pro generování URL na základě jmen koncových bodů.
- 'rest_framework.test.APITestCase': Zajišťuje testovací framework pro REST API.
"""

import json
from django.urls import reverse
from rest_framework.test import APITestCase

class WikiApiTestCase(APITestCase):
    """
    Testovací třída pro testování API koncových bodů wiki aplikace.
    Obsahuje testy pro úspěšné načtení článku, vyhledávání článků
    a test pro případ, kdy článek není nalezen.
    """

    def test_get_article_success(self):
        """
        Testuje úspěšné načtení článku.
        Ověřuje, že API vrátí status 200 a obsahuje klíč 'result' v odpovědi.
        """
        response = self.client.get(reverse('get_article', args=['Python']),
                                   HTTP_ACCEPT_LANGUAGE='en')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)

    def test_search_article(self):
        """
        Testuje vyhledávání článků pomocí API.
        Ověřuje, že API přesměruje (status 303) a vrátí seznam článků v odpovědi.
        """
        response = self.client.get('/wiki/some_search/')
        self.assertEqual(response.status_code, 303)
        data = response.json()
        self.assertIn('articles', data)

    def test_article_not_found(self):
        """
        Testuje případ, kdy hledaný článek neexistuje.
        Ověřuje, že API vrátí status 404 a neobsahuje klíč 'result' v odpovědi.
        """
        response = self.client.get(reverse('get_article', args=['nonexistentarticle']),
                                    HTTP_ACCEPT_LANGUAGE='en')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertNotIn('result', data)
