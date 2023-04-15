from rest_framework import permissions
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views import View

class LoginView(DjangoLoginView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        form = LoginForm()
        return render(request, '../Template/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('authenticated_home')
            else:
                form.add_error(None, '유효하지 않은 닉네임이나 패스워드입니다.')
        return render(request, '../Template/login.html', {'form': form})

class RegisterView(DjangoLoginView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        form = RegisterForm()
        return render(request, '../Template/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        return render(request, '../Template/register.html', {'form': form})