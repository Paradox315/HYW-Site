from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from user.simple_avatar import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20)
    avatar = models.CharField(max_length=100)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


def get_avatar(self):
    name = get_nickname_or_username(self)
    profile = Profile.objects.get(user=self)
    if profile.avatar is None or profile.avatar == '':
        profile.avatar = get_avatar_html(name, 48)
    return profile.avatar


def get_message_avatar(self):
    name = get_nickname_or_username(self)
    profile = Profile.objects.get(user=self)
    return get_avatar_html(name, 24)


User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
User.get_avatar = get_avatar
User.get_message_avatar = get_message_avatar
