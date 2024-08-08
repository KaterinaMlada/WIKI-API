"""
Modul obsahuje definici URL vzorů pro aplikaci wiki.

Importované knihovny:
'path' z 'django.urls': Používá se pro definování URL vzorů a mapování views.
'get_article' z 'wiki.views': Funkce, která zpracovává požadavek na získání článku podle jeho názvu.

URL vzory:
- 'wiki/<str:title>/': Mapuje URL na funkci 'get_article', 
která zpracovává dotazy na konkrétní články.
"""


from django.urls import path
from wiki.views import get_article

urlpatterns = [
    path(r'wiki/<str:title>/', get_article, name='get_article'),
]
