from rest_framework import serializers

from .models import Users

class TransferSerializer(serializers.Serializer):
    user_from = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    inn_to    = serializers.IntegerField()
    amount    = serializers.FloatField()
