from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.db.models import Q

# Create your views here.
def empdash(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    file_init = File.objects.filter(initiated_by = emp).count()
    pending_files = File.objects.filter(current_holder=emp, status="OPEN").count()
    closed_files = File.objects.filter(initiated_by =emp, status="CLOSE").count()
    context = {
        'eid' : eid,
        'emp' :emp,
        'file_init' : file_init,
        'pending_files' : pending_files,
        'closed_files' : closed_files,
    }
    return render(request, "empdash.html", context)
    
def emplogout(request):
    if 'eid' in request.session:
        del request.session['eid']
        messages.success(request,"Logged out successfully")
        return redirect("userlogin")
    else:    
        return redirect("userlogin")

def viewprofile(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    context = {
        'eid' : eid,
        'emp' : emp,
    }
    return render(request, "viewprofile.html", context)

def updateprofile(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    context = {
        'eid' : eid,
        'emp' : emp,
    }
    if request.method == "POST":
        name = request.POST.get("name")
        contactno = request.POST.get("contactno")
        picture = request.FILES.get("picture")
        address = request.POST.get("address")
        emp.name = name
        emp.contactno = contactno
        if picture:
            emp.picture = picture
        emp.address = address
        emp.save()
        messages.success(request, "Profile updated successfully")
        return redirect('viewprofile')
    return render(request, "updateprofile.html", context)

def initiatefile(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email = eid)
    employees = Employee.objects.all()
    context = {
        'eid' : eid,
        'employees':employees
    }
    if request.method == "POST":
        title = request.POST.get("title")
        subject = request.POST.get("subject")
        file_attachment = request.FILES.get("file_attachment")
        emp_id = request.POST.get("emp_id")
        forwarded_to = Employee.objects.get(email=emp_id)
        fi = File.objects.create(title=title, subject=subject, file_attachment=file_attachment, initiated_by=emp,current_holder=forwarded_to)
        FileMovement.objects.create(file=fi, from_employee=emp, to_employee=forwarded_to, action="CREATE", remarks="File created successfullt")
        messages.success(request, "File initiated successfully")
    return render(request, "initiatefile.html", context)

def viewfiles(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email = eid)
    files = File.objects.filter(initiated_by = emp)
    context = {
        'eid' : eid,
        'files' : files,
    }
    return render(request, "viewfiles.html", context)


def receivedfiles(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email = eid)
    files = File.objects.filter(Q(current_holder=emp) & Q(status = "OPEN"))
    context = {
        'eid' : eid,
        'files' : files,
        'emp' : emp,
    }
    return render(request, "receivedfiles.html", context)


def filedetails(request, fid):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email = eid)
    file = File.objects.get(file_no = fid)
    employees = Employee.objects.all()
    file_movements = FileMovement.objects.filter(file = file)
    context = {
        'eid' : eid,
        'file' : file,
        'emp' : emp,
        'employees' : employees,
        'file_movements' : file_movements,
    }
    if request.method == "POST":
        emp_email = request.POST.get("emp_email")
        action = request.POST.get("action")
        remarks = request.POST.get("remarks")
        to_employee = Employee.objects.get(email=emp_email)
        FileMovement.objects.create(file=file,from_employee=emp,to_employee=to_employee,action=action,remarks=remarks)
        file.current_holder = to_employee
        file.save()
        messages.success(request, f"File {action} to {to_employee.name}")
        return redirect("receivedfiles")
    return render(request, "filedetails.html", context)

def closefile(request, fid):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email = eid)
    file = File.objects.get(file_no = fid)
    file.status = "CLOSE"
    file.save()
    messages.success(request, "File closed successfully")
    return redirect("receivedfiles")

def emppass(request):
    if 'eid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('userlogin')
    eid = request.session.get('empid')
    context = {
        'eid' : eid,
    }
    if request.method == "POST":
        oldpwd = request.POST.get("oldpwd")
        newpwd = request.POST.get("newpwd")
        cnfpwd = request.POST.get("cnfpwd")
        emp = LoginInfo.objects.get(username=eid)
        if newpwd != cnfpwd:
            messages.warning(request, "Enter same password")
            return redirect("emppass")
        if oldpwd != emp.password:
            messages.error(request, "Old password is incorrect")
            return redirect("emppass")
        if newpwd != emp.password:
            messages.warning(request, "You cannot set previous password")
            return redirect("emppass")
        emp.password = newpwd
        emp.save()
        messages.success(request, "Password change successfully")
        return redirect("emppass")
        
    return render(request, "emppass.html", context)