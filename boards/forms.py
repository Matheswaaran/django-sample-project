from django import forms

from .models import Topic


class CreateNewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter subject of the topic here'}
        )
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']