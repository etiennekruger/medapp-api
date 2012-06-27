from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=255)
    rate = models.FloatField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'currencies'

    def __unicode__(self):
        return '%s' % self.name

