from rest_framework import serializers
from lims_app.models import APIRequestLog

class APIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        fields = '__all__'


# from rest_framework import serializers
# from .models import APIRequestLog
#
# class APIRequestLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = APIRequestLog
#         fields = '__all__'
