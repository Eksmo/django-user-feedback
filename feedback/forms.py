from django import forms

from feedback.models import Feedback, FEEDBACK_TYPES

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('type', 'email', 'feedback',)

    type = forms.ChoiceField(choices=FEEDBACK_TYPES, 
        initial=FEEDBACK_TYPES[0][0], widget=forms.RadioSelect(attrs={
            'id':'feedback_type_id',
            #'class': 'pseudo-popup_input',
        }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
            'id':'feedback_email_id', 
            'class':'pseudo-popup_input',
        }))
    feedback = forms.CharField(widget=forms.Textarea(attrs={
            'id':'feedback_feedback_id', 
            'class':'pseudo-popup_input',
            'rows': '4',
        }))
