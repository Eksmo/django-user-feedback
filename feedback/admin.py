from django.contrib import admin

from feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    readonly_fields = ('url', 'email', 'user', 'timestamp', 'headers', \
        'ip_address')

    list_display = ('get_user', 'get_feedback', 'timestamp', 'type', \
        'resolved')

    list_editable = ('resolved',)
    list_filter = ('resolved', 'type', 'timestamp')
    search_fields = ['feedback', 'email']


    def get_user(self, object):
        return object.user if object.user else 'Anonymous'
        
    def get_feedback(self, object):
        return object.feedback[:100]

admin.site.register(Feedback, FeedbackAdmin)