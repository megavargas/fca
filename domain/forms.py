from django import forms

class InviteActionForm(forms.Form):
    emails = forms.CharField()
    text = forms.CharField()

class DeleteActionForm(forms.Form):
    id = forms.IntegerField()