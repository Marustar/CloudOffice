from django.shortcuts import render, redirect
from .models import Employee

def pending_registrations(request):
    if not request.user.is_staff:
        return redirect('home')

    pending_users = Employee.objects.filter(is_approved=False)
    return render(request, 'pending_registrations.html', {'pending_users': pending_users})

def approve_user(request, user_id):
    if not request.user.is_staff:
        return redirect('home')

    employee = Employee.objects.get(Emp_User__id=user_id)
    employee.is_approved = True
    employee.save()
    return redirect('pending_registrations')
