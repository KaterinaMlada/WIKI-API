from django.urls import path
from .views import get_article

urlpatterns = [
    path('wiki/<str:title>/', get_article, name='get_article'),
]
