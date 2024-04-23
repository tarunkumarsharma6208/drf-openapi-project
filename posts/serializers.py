from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    userId = serializers.IntegerField()
    body = serializers.CharField()
