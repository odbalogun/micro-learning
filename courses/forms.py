from .models import Modules, EnrolledModules
from django import forms


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Modules
        exclude = ('created_at', 'students')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].disabled = True
        self.fields['course'].disabled = True


class OpenEnrolledModuleForm(forms.ModelForm):
    class Meta:
        model = EnrolledModules
        exclude = ('date_activated', 'expires')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrolled'].disabled = True
        self.fields['user'].disabled = True



