from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'full_name',
            'name',

        )
    def get_full_name(self, obj):
        return obj.get_username()