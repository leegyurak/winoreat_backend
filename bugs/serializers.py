from rest_framework import serializers

from bugs.models import Answer, Bug


class ListBugsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bug
        fields = ("id", "bug_type", "title", "status_type")


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ("answer", "created")


class RetrieveBugSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Bug
        fields = (
            "id",
            "bug_type",
            "title",
            "status_type",
            "description",
            "answers",
            "created",
        )


class CreateBugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bug
        fields = ("bug_type", "title", "description", "email")

    def save(self, **kwargs):
        return Bug.objects.create(
            **self.validated_data,
            status_type=Bug.StatusType.REPORTED,
        )
