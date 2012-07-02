from django.db import models
from profile.models import Profile


class NeedExpert(models.Model):
    profile = models.ForeignKey(Profile)
    expert_type = models.CharField(max_length=255)
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Need expert'

    def __unicode__(self):
        return '%s' % self.profile.name


class NeedHelp(models.Model):
    profile = models.ForeignKey(Profile)
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Need help'

    def __unicode__(self):
        return '%s' % self.profile.name

