from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.CharField(required=False)
    status = serializers.CharField()