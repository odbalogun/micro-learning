from .models import Modules, EnrolledModules, Enrolled
from django import forms


class EnrolledForm(forms.ModelForm):
    course_fee = forms.FloatField(label='Course Fee', disabled=True, required=False)

    class Meta:
        model = Enrolled
        exclude = ('date_enrolled', 'initial_payment_type')


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



