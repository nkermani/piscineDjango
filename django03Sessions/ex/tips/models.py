from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    @property
    def reputation(self):
        tips = self.tip_set.all()
        rep = 0
        for tip in tips:
            rep += tip.upvotes.count() * 5
            rep -= tip.downvotes.count() * 2
        return rep


# Create your models here.
class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="upvoted_tips", blank=True
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="downvoted_tips", blank=True
    )

    def __str__(self):
        return self.content[:20]
