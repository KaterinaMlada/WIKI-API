from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

WIKIPEDIA_API_URL = "https://{lang}.wikipedia.org/w/api.php"

def fetch_wikipedia_article(title, lang='cs'):
    try:
        response = requests.get(WIKIPEDIA_API_URL.format(lang=lang), params={
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'exintro': True
        })
        response.raise_for_status()
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        page = next(iter(pages.values()), {})
        return page
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def search_wikipedia_articles(query, lang='cs'):
    try:
        response = requests.get(WIKIPEDIA_API_URL.format(lang=lang), params={
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'utf8': 1
        })
        response.raise_for_status()
        data = response.json()
        search_results = data.get('query', {}).get('search', [])
        return [{'name': result['title']} for result in search_results]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

@api_view(['GET'])
def get_article(request, title):
    lang = request.headers.get('Accept-Language', 'cs',).split(',')[0] 
    article = fetch_wikipedia_article(title, lang)
    
 
    if article.get('missing') is None:
        extract = article.get('extract', '')
  
        if 'text/html' in request.headers.get('Accept', ''):
            return render(request, 'article.html', {'title': title, 'result': extract})
    
        return Response({'result': extract}, status=200)
    
   
    search_results = search_wikipedia_articles(title, lang)
    
    if search_results:
    
        if 'text/html' in request.headers.get('Accept', ''):
            return render(request, 'article.html', {'articles': search_results})

        return Response({'articles': search_results}, status=303)
    

    if 'text/html' in request.headers.get('Accept', ''):
        return render(request, 'article.html', {'result': 'No results found'})
    return Response({}, status=404)
