from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


FEEDBACK_TYPES = (
    ('bug', _('Bug')),
    ('feature', _('Feature')),
    ('support', _('Support request')),
)

class Feedback(models.Model):
    feedback = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    url = models.URLField(blank=True, verify_exists=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    resolved = models.BooleanField(default=False)
    type = models.CharField(max_length=128, blank=True, \
        choices=getattr(settings, 'FEEDBACK_TYPES', FEEDBACK_TYPES))
    headers = models.TextField(blank=True, null=True)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)

    class Meta:
        ordering = ['-timestamp',]
        verbose_name_plural = _('Feedback')

    def __unicode__(self):
        return _('Feedback from %(user)s sent %(date)s') % \
            {'user':self.user if self.user else 'Anonymous', 'date': self.timestamp}
