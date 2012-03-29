from feedback.forms import FeedbackForm

def feedback_form(request):
    return {'feedback_form': FeedbackForm(
        initial={'email':request.user.email \
            if hasattr(request, 'user') and request.user.is_authenticated() and \
                request.user.email else None}
    )}
