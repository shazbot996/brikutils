from django.forms import ModelForm
from django import forms
from .models import Org, Assessment


class OrgAddForm(ModelForm):
    class Meta:
        model = Org
        exclude = ('org_creator',)


class AssessAddForm(ModelForm):
    class Meta:
        model = Assessment
        exclude = ('assess_creator',)

    def __init__(self, user, *args, **kwargs):
        super(AssessAddForm, self).__init__(*args, **kwargs)
        self.fields['assess_org'].queryset = Org.objects.filter(org_creator=user)

# raise ValidationError("Invalid Something") -

class OrgUpdateForm(forms.Form):
    org_name = forms.CharField()
    org_email = forms.CharField(widget=forms.Textarea)
