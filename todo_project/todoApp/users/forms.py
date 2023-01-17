from django import forms
from .models import UserInfo


class DateInput(forms.DateInput):
    input_type = 'date'


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = "__all__"
        widgets = {
            'target_date': DateInput()
        }

        exclude = ('completed_task',"percentage","first_name",)

    # def __str__(self):
    #     return self.task_description
