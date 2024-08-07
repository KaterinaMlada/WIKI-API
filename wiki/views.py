from typing import List, Dict, Optional, Union
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

WIKIPEDIA_API_URL = 'https://{lang}.wikipedia.org/w/api.php'

def fetch_wikipedia_article(title: str, lang: str = 'cs') -> Dict[str, Union[str, Dict]]:
    #Funkce pro získání článku z Wikipedie podle názvu a jazyka.
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
        print(f'Request failed: {e}')
        return {}

def search_wikipedia_articles(query: str, lang: str = 'cs') -> List[Dict[str, str]]:
    #Funkce pro vyhledání článků na Wikipedii podle dotazu a jazyka.
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
        print(f'Request failed: {e}')
        return []
    
def validate_language(lang: str) -> str:
#Funkce pro validaci jazyka, vrací 'en' pokud jazyk není podporován.
    supported_languages = {'en', 'cs'}

    return lang if lang in supported_languages else 'en'

@api_view(['GET'])
def get_article(request, title: str) -> Response:
    #API view pro získání článku z Wikipedie nebo vyhledání článků podle názvu.
    lang = request.headers.get('Accept-Language', 'en').split(',')[0].split('-')[0]
    print(f'Requested language: {lang}')

    article = fetch_wikipedia_article(title, lang)
    extract = ''
    articles = []
    status_code = 200

    if article.get('missing') is None:
        extract = article.get('extract', '').split('</p>', 1)[0] + '</p>'
        print(f'Extract before cleaning: {extract}')
        if not extract.strip() or 'mw-empty-elt' in extract:
            print('Extract is empty or meaningless')
            extract = ''
    else:
        articles = search_wikipedia_articles(title, lang)
        print(f'Search results: {articles}')
        if articles:
            status_code = 303
        else:
            status_code = 404

    if not extract and not articles:
        extract = 'No results found'
        status_code = 404

    if 'text/html' in request.headers.get('Accept', ''):
        context = {'title': title, 'result': extract} if extract else {'articles': articles}
        return render(request, 'article.html', context)
    
    response_data = {'result': extract} if extract else {'articles': articles}
    return Response(response_data, status=status_code)