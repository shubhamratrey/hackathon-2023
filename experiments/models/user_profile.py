import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (User, Permission)


class UserProfile(User):
    """
    UserProfile is the extension of AbstractUser to add ZoopZam based functionality to auth.User
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    )

    phone = models.CharField(max_length=25, db_index=True, blank=True, null=True, default=None, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, default=None)
    firebase_uid = models.CharField(max_length=50, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    signedup_on = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(null=True, default=None)
    status = models.CharField(max_length=250, blank=True)
    anonymous = models.BooleanField(default=False)
    avatar = models.CharField(max_length=250, blank=True, null=True)
    firebase_signin_provider = models.CharField(max_length=25, null=True)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_user_doc(self):
        return {
            'id': self.id,
            'name': self.get_full_name(),
            'original_avatar': self.avatar if self.avatar else None,
        }

    def get_jwt_token(self):
        return jwt.encode({'user_id': self.id}, settings.JWT_KEY, algorithm='HS512')
