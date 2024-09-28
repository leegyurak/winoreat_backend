from django.db import models
from django_extensions.db.models import TimeStampedModel


class Bug(TimeStampedModel):
    class BugType(models.TextChoices):
        RESTAURANT_NOT_FOUND = "RESTAURANT_NOT_FOUND", "식당을 찾을 수 없어요."
        WRONG_RESTAURANT_IMAGE = "WRONG_RESTAURANT_IMAGE", "식당 이미지들이 이상해요."
        ADVERTISEMENT_DOUBT = "ADVERTISEMENT_DOUBT", "광고가 의심돼요."
        NOT_RESTAURANT_PLACE = "NOT_RESTAURANT_PLACE", "이 장소는 식당이 아니에요."
        SERVICE_NOT_WORKED = "SERVICE_NOT_WORKED", "서비스가 정상 동작하지 않아요."

    class StatusType(models.TextChoices):
        REPORTED = "REPORTED", "제보 완료"
        DONE = "DONE", "조치 완료"

    email = models.EmailField(verbose_name="답변 받을 이메일", null=True)
    bug_type = models.CharField(
        verbose_name="버그 유형", choices=BugType.choices, max_length=127
    )
    status_type = models.CharField(
        verbose_name="버그 상태 유형", choices=StatusType.choices, max_length=127
    )
    title = models.CharField(verbose_name="제목", max_length=63)
    description = models.CharField(verbose_name="내용", max_length=1023)


class Answer(TimeStampedModel):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField("처리 내용", max_length=1023)
