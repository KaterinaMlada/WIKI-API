from django.urls import path
from .views import get_article

urlpatterns = [
    path(r'wiki/<str:title>/', get_article, name='get_article'),
]
