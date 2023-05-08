from rest_framework import permissions
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from Emp.models import Employee, Department
from django.contrib import messages # 메시지 기능 추가
from django.views.decorators.csrf import csrf_exempt

class LoginView(DjangoLoginView):
    permission_classes = (permissions.AllowAny)
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})  # 경로 변경
        
def index(request):
        return render(request, 'index.html')

@csrf_exempt
def upgrade_reply(request):

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                try:
                    print(user)
                    employee = Employee.objects.get(Emp_User=user)
                    if employee.is_approved:
                        login(request, user)
                        return redirect('authenticated_home')
                    else:
                        form.add_error(None, '계정이 아직 승인되지 않았습니다. 관리자의 승인을 기다려주세요.')
                        
                        return render(request, 'login')
                        return redirect('login')
                except Employee.DoesNotExist:
                    form.add_error(None, '계정 정보를 찾을 수 없습니다.')
                    return redirect('login')
            else:
                form.add_error(None, '유효하지 않은 닉네임이나 패스워드입니다.')
        return render(request, '../Template/login.html', {'form': form})

class RegisterView(DjangoLoginView):
    permission_classes = (permissions.AllowAny)
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})  # 경로 변경

    def post(self, request):
        form = RegisterForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            emp = Employee()
            emp.Emp_User = user
            emp.Emp_Rank = 1
            emp.is_approved = False  # 관리자 승인해야 로그인 가능
            emp.save()
            user.save()
            
            messages.success(request, '회원가입이 완료되었습니다. 승인이 완료되면 로그인할 수 있습니다.')
            login(request, user)
            return redirect('login')
        else:
            print('not valid')

        return render(request, 'register.html', {'form': form})

