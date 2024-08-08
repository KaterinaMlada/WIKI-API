"""
Importuje serializers z Django REST frameworku.

'serializers': Poskytuje třídy a funkce pro serializaci a deserializaci dat,
 které usnadňují konverzi mezi komplexními datovými typy a JSON.
"""

from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):

    """
    Pro serializaci/deserializaci dat článků v aplikaci wiki.

    Políčka:
    - 'result': CharField, které uchovává řetězec obsahující výsledek.
    - 'articles': ListField, které obsahuje seznam slovníků.(články)

    """

    result = serializers.CharField(required=False)
    articles = serializers.ListField(child=serializers.DictField(), required=False)
