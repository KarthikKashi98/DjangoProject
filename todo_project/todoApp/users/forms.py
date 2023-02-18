from django import forms
from .models import UserInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ["username","email","password1","password2"]:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
