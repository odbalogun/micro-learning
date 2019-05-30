from .models import Modules
from django import forms


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Modules
        exclude = ('created_at', 'students')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].disabled = True
        self.fields['course'].disabled = True


