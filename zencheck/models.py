from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class PulseCheck(models.Model):
    pulse_check_date = models.DateTimeField(auto_now_add=True)
    question_1 = models.IntegerField(default=3)
    question_2 = models.IntegerField(default=3)
    question_3 = models.IntegerField(default=3)
    question_4 = models.IntegerField(default=3)
    question_5 = models.IntegerField(default=3)
    question_6 = models.IntegerField(default=3)
    question_7 = models.IntegerField(default=3)
    question_8 = models.IntegerField(default=3)
    question_9 = models.IntegerField(default=3)
    question_10 = models.IntegerField(default=3)
    question_11 = models.IntegerField(default=3)
    question_12 = models.IntegerField(default=3)
    question_13 = models.IntegerField(default=3)
    question_14 = models.IntegerField(default=3)
    question_15 = models.IntegerField(default=3)
    question_16 = models.IntegerField(default=3)
    question_17 = models.IntegerField(default=3)
    question_18 = models.IntegerField(default=3)
    question_19 = models.IntegerField(default=3)
    question_20 = models.IntegerField(default=3)
    question_21 = models.IntegerField(default=3)
    question_22 = models.IntegerField(default=3)
    question_23 = models.IntegerField(default=3)
    question_24 = models.IntegerField(default=3)
    question_25 = models.IntegerField(default=3)
    question_26 = models.IntegerField(default=3)
    question_27 = models.IntegerField(default=3)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    time_submitted = models.DateTimeField()
  
    def __str__(self):
        return '%s - %s - %s' % (self.pulse_check_date, self.user, self.pk)

class News(models.Model):
    title = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024, null=True)
    source = models.CharField(max_length=1024, null=True)
    description = models.TextField(null=True)
    url = models.CharField(max_length=4096)
    image = models.CharField(max_length=4096, null=True)
    publish_at = models.DateTimeField()
    content = models.TextField(null=True)
    update_at = models.DateTimeField(auto_now=True)
    is_top_headlines = models.BooleanField(default=True)

class Tweets(models.Model):
    tweet_id = models.IntegerField()
    username = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)
    user_profile_photo = models.CharField(max_length=4096)
    text = models.CharField(max_length=4096)
    url = models.CharField(max_length=4096)
    media_url = models.CharField(max_length=4096, null=True, default=None)
    created_at = models.DateTimeField()

class WellBeing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Q1 = models.TextField(null=True)
    Q2 = models.TextField(null=True)
    Q3 = models.TextField(null=True)
    Q4 = models.TextField(null=True)
    Q5 = models.TextField(null=True)
    Q6 = models.TextField(null=True)
    Q7 = models.TextField(null=True)
    Q8 = models.TextField(null=True)
