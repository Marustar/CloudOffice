from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Emp.models import Employee, Department
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label='아이디')
    email = forms.EmailField(max_length=254, required=True, label='이메일')
    Emp_Name = forms.CharField(max_length=10, required=True, label='사원 이름')
    class Meta:
        model = User
        fields = ('username', 'email', 'Emp_Name','password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.save()

        emp_name = self.cleaned_data.get('Emp_Name')

        employee = Employee(Emp_User=user, Emp_Name=emp_name,is_approved=False)
        employee.save()
        
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("이미 존재하는 계정입니다.")
        return username
