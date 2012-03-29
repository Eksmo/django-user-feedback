from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import CreateView

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FeedbackView(CreateView):
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    header_filter = getattr(settings, 'FEEDBACK_HEADER_FILTER',
        (
            'CONTENT_TYPE',
            'HTTP_ACCEPT',
            'HTTP_ACCEPT_CHARSET',
            'HTTP_ACCEPT_ENCODING',
            'HTTP_ACCEPT_LANGUAGE',
            'HTTP_CACHE_CONTROL',
            'HTTP_CONNECTION',
            'HTTP_HOST',
            'HTTP_KEEP_ALIVE',
            'HTTP_REFERER',
            'HTTP_USER_AGENT',
            'QUERY_STRING',
            'REMOTE_ADDR',
            'REMOTE_HOST',
            'REQUEST_METHOD',
            'SCRIPT_NAME',
            'SERVER_NAME',
            'SERVER_PORT',
            'SERVER_PROTOCOL',
            'SERVER_SOFTWARE',
            'HTTP_COOKIE',
        )
    )

    def get_initial(self):
        if self.request.user.is_authenticated() and \
            self.request.user.email:
            return {'email': self.request.user.email}
        return {}

    def get_form_kwargs(self):
        kwargs = super(FeedbackView, self).get_form_kwargs()
        headers = "\n".join(
                ['='.join([k, self.request.META[k]]) for k in self.header_filter if k in self.request.META]
            )
        instance = Feedback(
            url = self.request.POST.get('url', self.request.META.get('HTTP_REFERER', '')),
            user = self.request.user if self.request.user.is_authenticated() else None,
            headers = unicode(headers),
            ip_address = self.request.META.get('REMOTE_ADDR', '')
        )
        kwargs.update({
            'instance': instance,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        if kwargs.get('form'):
            kwargs['feedback_form'] = kwargs['form']
        return kwargs

    def form_valid(self, *args, **kwargs):
        response = super(FeedbackView, self).form_valid(*args, **kwargs)

        if getattr(settings, 'FEEDBACK_SEND_EMAIL', False) and \
            getattr(settings, 'FEEDBACK_TO_EMAIL', False):
            context = {"feedback":self.object}
            EmailMultiAlternatives(
                    render_to_string('feedback/email/subject.txt', context),
                    render_to_string('feedback/email/body.txt', context),
                    settings.DEFAULT_FROM_EMAIL,
                    getattr(settings, 'FEEDBACK_TO_EMAIL'),
                ).send(fail_silently=False)

        if getattr(settings, 'FEEDBACK_FLASH_MESSAGE', False) and \
            'django.contrib.messages' in settings.INSTALLED_APPS:
            messages.success(self.request, _('Your feedback has been sent. Thank you!'))
        return response

    def form_invalid(self, form):
        # Update our context to avoid being overwritten by context processors
        context = RequestContext(self.request, self.get_context_data())
        context['feedback_form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        return self.request.META.get(
            'HTTP_REFERER',
            getattr(settings, 'FEEDBACK_SUCCESS_URL', '/')
        )
