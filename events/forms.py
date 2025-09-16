# events/forms.py
from django import forms
from .models import Participation

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a note or comment...'}),
        }