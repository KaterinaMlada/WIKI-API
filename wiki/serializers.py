from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    result = serializers.CharField(required=False)
    articles = serializers.ListField(child=serializers.DictField(), required=False)
