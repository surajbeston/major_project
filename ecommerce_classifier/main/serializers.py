from rest_framework import serializers

class CategorizeSerializer(serializers.Serializer):
    title = serializers.CharField(required = False)
    price = serializers.FloatField( required = False)
    description = serializers.CharField(required = False)
