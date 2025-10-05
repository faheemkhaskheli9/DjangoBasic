# messaging/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class NewThreadForm(forms.Form):
    to = forms.ModelChoiceField(queryset=User.objects.none(), label="Send to")
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Message")

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user")
        super().__init__(*args, **kwargs)
        self.fields["to"].queryset = User.objects.exclude(id=current_user.id)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a message…"})}
