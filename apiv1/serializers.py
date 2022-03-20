from rest_framework import serializers


class TaskStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200)
    detail = serializers.CharField(max_length=200)
