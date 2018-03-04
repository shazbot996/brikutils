from django.forms import ModelForm

from .models import VMdata


class VMdataForm(ModelForm):
    class Meta:
        model = VMdata
        exclude = ('rvt_user',)

# raise ValidationError("Invalid Something") -