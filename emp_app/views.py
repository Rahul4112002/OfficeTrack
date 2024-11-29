from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from django.contrib import messages
from django.db.models import Q

def home(request):
    return render(request,'home.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps,
    }
    print(context)
    return render(request,'view_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = int(request.POST.get('salary', 0))  # Provide default value to avoid ValueError
        bonus = int(request.POST.get('bonus', 0))    # Provide default value to avoid ValueError
        dept = int(request.POST.get('dept')  )     # Use the correct name from the form field
        role = int(request.POST.get('role'))
        hire_date = request.POST.get('hire_date')
        phone = int(request.POST.get('phone', 0))
        try:
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                dept_id=dept,
                role_id=role,
                hire_date=hire_date,
                phone=phone,
            )
            new_emp.save()
            messages.success(request, "Employee added successfully!")
            return render(request, 'add_emp.html')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'add_emp.html')

    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        messages.error(request, "An error occurred! Employee has not been added.")
        return render(request, 'add_emp.html')

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_remove = Employee.objects.get(id=emp_id)
            emp_to_be_remove.delete()
            messages.success(request, "Employee Removed successfully!")
            
        except:
            messages.error(request, "Please enter valid Employe ID")
            return render(request, 'remove_emp.html')
            
    emps = Employee.objects.all()
    context = {
        'emps': emps,
    }
    return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        dept = request.POST.get('dept')
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(Q(dept__name__icontains= dept))
        if role:
            emps = emps.filter(Q(role__name__icontains = role))
            
        context = {
            'emps': emps,
        }
        return render(request, 'view_emp.html',context)
    else:
        return render(request,'filter_emp.html')
