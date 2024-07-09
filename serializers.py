# serializers.py

from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    tid = serializers.CharField(max_length=100)
    assigned_to = serializers.IntegerField()  # Assuming assigned_to is an ID
    assigned_by = serializers.IntegerField()  # Assuming assigned_by is an ID
    description = serializers.CharField(max_length=1000)
