from rest_framework import permissions
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views import View
from Emp.models import Employee, Department
from django.contrib import messages 

class LoginView(DjangoLoginView):
    permission_classes = (permissions.AllowAny,)
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('authenticated_home')
            else:
                form.add_error(None, '유효하지 않은 닉네임이나 패스워드입니다.')
                return render(request, 'login.html', {'form': form})
        else:
            form.add_error(None, '유효하지 않은 닉네임이나 패스워드입니다.')
            return render(request, 'login.html', {'form': form})
            
def index(request):
    return render(request, 'index.html')


class RegisterView(DjangoLoginView):
    permission_classes = (permissions.AllowAny,)
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            emp = Employee()
            emp.Emp_User = user
            emp.Emp_Rank = 1
            emp.is_approved = False  # 관리자 승인해야 로그인 가능
            messages.success(request, '회원가입이 완료되었습니다. 승인이 완료되면 로그인할 수 있습니다.')
            return redirect('login')
        else:
            messages.error(request, '회원가입에 실패하였습니다. 다시 시도해주세요.')
            return render(request, 'register.html', {'form': form})
