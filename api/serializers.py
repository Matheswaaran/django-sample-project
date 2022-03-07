from rest_framework import serializers

from boards.models import Board, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'subject', 'is_active', 'created_at', 'updated_at']


class BoardSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at', 'topics']
