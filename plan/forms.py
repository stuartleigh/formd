from django import forms

from .models import Plan


class ChangePlanForm(forms.Form):
    plan = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ChangePlanForm, self).__init__(*args, **kwargs)

    def clean_plan(self):
        key = self.cleaned_data['plan']
        try:
            self.plan = Plan.objects.get(key=key)
        except Plan.DoesNotExist:
            raise forms.ValidationError("Invalid plan {}".format(key))

    def save(self):
        self.user.set_plan(self.plan)