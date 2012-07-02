from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Profile'

    def __unicode__(self):
        return '%s' % self.name

