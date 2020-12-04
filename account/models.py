from django.db import models
from django.conf import settings
import os


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def save(self, *args, **kwargs):
        old_photo = Profile.objects.get(pk=self.pk).photo
        if old_photo:
            try:
                os.remove(old_photo.path)
            except FileNotFoundError:
                pass
        super().save(*args, **kwargs)
