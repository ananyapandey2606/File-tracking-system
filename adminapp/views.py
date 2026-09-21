from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *

# Create your views here.
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    file_count = File.objects.all().count()
    pending_files = File.objects.filter(status = "OPEN").count()
    total_dept = Department.objects.all().count()
    total_emp = Employee.objects.all().count()
    context = {
        'adminid' : adminid,
        'file_count' : file_count,
        'pending_files' : pending_files,
        'total_dept' : total_dept,
        'total_emp' : total_emp,
    }
    return render(request, "admindash.html", context)
    return render(request, "admindash.html")
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"Logged out successfully")
        return redirect("adminlogin")
    else:    
        return redirect("adminlogin")

    
def adddept(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid,
    }
    if request.method == "POST":
        dept_name = request.POST.get('dept_name')
        if Department.objects.filter(dept_name=dept_name):
            messages.warning(request, "This department already exists")
            return redirect("adddept")
        dep = Department(dept_name=dept_name)
        dep.save()
        messages.success(request, "Department added successfully")
        return redirect("viewdept")
    return render(request, "adddept.html", context)

def viewdept(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    depts = Department.objects.all()
    context = {
        'adminid' : adminid,
        'depts' :depts,
    }
    return render(request, "viewdept.html", context)

def addemp(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    depts = Department.objects.all()
    context = {
        'adminid' : adminid,
        'depts' : depts,
    }
    if request.method == "POST":
        empid = request.POST.get('empid')
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        designation = request.POST.get('designation')
        dept_id = request.POST.get('dept_id')
        dept = Department.objects.get(id=dept_id)
        if LoginInfo.objects.filter(username=email):
            messages.warning(request, "This email already exists")
            return redirect("addemp")
        log = LoginInfo.objects.create(usertype='employee',username=email,password="12345678")
        emp = Employee.objects.create(log=log, empid=empid, name=name, contactno=contactno, email=email, designation=designation, department=dept)
        messages.success(request, "Employee Added successfully")
        return redirect("viewemp")
    return render(request, "addemp.html", context)

def viewemp(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    emps = Employee.objects.all()
    context = {
        'adminid' : adminid,
        'emps' : emps,
    }
    return render(request, "viewemp.html", context)

def adminpass(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid,
    }
    if request.method == "POST":
        oldpwd = request.POST.get("oldpwd")
        newpwd = request.POST.get("newpwd")
        cnfpwd = request.POST.get("cnfpwd")
        admin = LoginInfo.objects.get(username=adminid)
        if newpwd != cnfpwd:
            messages.warning(request, "Enter same password")
            return redirect("adminpass")
        if oldpwd != admin.password:
            messages.error(request, "Old password is incorrect")
            return redirect("adminpass")
        if newpwd != admin.password:
            messages.warning(request, "You cannot set previous password")
            return redirect("adminpass")
        admin.password = newpwd
        admin.save()
        messages.success(request, "Password change successfully")
        return redirect("adminpass")
        
    return render(request, "adminpass.html", context)

def deldept(request, did):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    if Department.objects.filter(id=did):
        Department.objects.get(id=did).delete()
        messages.success(request, "Department deleted successfully")
        return redirect("viewdept")
    else :
        return redirect("viewdept")


def allfiles(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    files = File.objects.all()
    context = {
        'adminid' : adminid,
        'files' :files,
    }
    return render(request, "allfiles.html", context)