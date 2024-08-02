from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests


WIKIPEDIA_API_URL = "https://{lang}.wikipedia.org/w/api.php"  

def fetch_wikipedia_article(title, lang='en'):
    response = requests.get(WIKIPEDIA_API_URL.format(lang=lang), params={
      
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'exintro': True
    })
    data = response.json()
    pages = data.get('query', {}).get('pages', {})
    page = next(iter(pages.values()), {})
    return page

def search_wikipedia_articles(query, lang='en'):
    response = requests.get(WIKIPEDIA_API_URL.format(lang=lang), params={
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'utf8': 1
    })
    data = response.json()
    search_results = data.get('query', {}).get('search', [])
    return [{'name': result['title']} for result in search_results]

@api_view(['GET'])
def get_article(request, title):
    lang = request.headers.get('Accept-Language', 'en')
    article = fetch_wikipedia_article(title, lang)
    
    if article.get('missing') is None:
        extract = article.get('extract', '')
        return Response({'result': extract}, status=200)
    
    search_results = search_wikipedia_articles(title, lang)
    
    if search_results:
        return Response({'articles': search_results}, status=303)  
    
    return Response({}, status=404)  
