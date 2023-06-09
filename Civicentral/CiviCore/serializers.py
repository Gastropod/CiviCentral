from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import (
    User,
    Category,
    Discussion,
    Comment,
    Issue,
    Vote,
    Endorsement,
    ExpertAnalysis,
    Notification,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "location",
            "date_joined",
            "is_active",
            "is_staff",
            "last_login",
            "avatar_url",
            "bio",
            "date_of_birth",
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description")

class DiscussionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Discussion
        fields = (
            "id",
            "title",
            "description",
            "created_by",
            "created_at",
            "updated_at",
            "category",
            "status",
        )

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    total_votes = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "created_by",
            "created_at",
            "updated_at",
            "discussion",
            "parent_comment",
            "replies",
            "total_votes",
        )
        read_only_fields = ("replies",)

    def create(self, validated_data):
        user = self.context["created_by"]
        comment = Comment.objects.create(created_by=user, **validated_data)
        return comment

    def get_replies(self, obj):
        replies = obj.comment_set.all()
        return CommentSerializer(replies, many=True, read_only=True).data

    def get_votes(self, obj):
        comment_content_type = ContentType.objects.get_for_model(Comment)
        votes = Vote.objects.filter(content_type=comment_content_type, object_id=obj.id)
        return VoteSerializer(votes, many=True, read_only=True).data

    replies = serializers.SerializerMethodField()


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ("id", "title", "description", "created_at", "updated_at", "created_by")
        
class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Vote
        fields = ("id", "user", "vote_type", "content_type", "object_id")

class EndorsementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endorsement
        fields = ("id", "endorser", "endorsee", "issue", "created_at")

class ExpertAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertAnalysis
        fields = ("id", "author", "issue", "title", "content", "created_at", "updated_at")

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "user", "notification_type", "element_id", "is_read", "created_at")
