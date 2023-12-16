from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from account.models import *
from bookapp.models import *

# Create your views here.
def student_signup(request):
    if request.method == 'POST':

        name = request.POST['name']
        roll = request.POST['roll']
        dept = request.POST['dept']
        phone_no = request.POST['ph']
        reg = request.POST['reg']
        address =request.POST['addr']
        password = make_password(request.POST['password'],salt='101')

        std_obj= Student.objects.filter(reg=reg)
        if len(std_obj) != 0:
            context = {
                'error': 'Registration number was alreadry used',
                'status':True
            }
            return render(request, 'student_signup.html', context)
        
        std_obj= Student.objects.all().order_by('-sid')[:1]
        if len(std_obj) != 0:
            sid=std_obj[0].uid + 1
        else:
            sid=1

        Student.objects.create(
            sid =sid,
            name = name,
            phone_no = phone_no,
            dept=dept,
            reg = reg,
            password = password,
            roll = roll,
            address=address

        )
        std_obj= Student.objects.filter(reg=reg)

        context={
            'status':False,
            'info':'Your student_id is: '+str(std_obj[0].sid)
        }
        return render(request, 'signup_comp.html',context)

    return render(request, 'student_signup.html')

def student_login(request):
    if 'sid' in request.session:
        return redirect(std_dashboard)
    
    if request.method == 'POST':
        sid = request.POST['sid']
        password = request.POST['password']
        try:
            std_obj = Student.objects.get(sid=sid)
            if check_password(password, std_obj.password):
                if not std_obj.active:
                    context= {
                        'error':'You are not Verified',
                        'status':True
                    }

                    return render(request, 'student_login.html',context)
                else:
                    request.session['sid'] = std_obj.sid
                    return redirect(std_dashboard)
            else:
                context= {
                    'error':'student id or password is wrong',
                    'status':True
                }
                return render(request, 'student_login.html',context)
        except:
            context= {
                'error':'student id or password is wrong',
                'status':True
            }
            return render(request, 'student_login.html',context)

    return render(request, 'student_login.html')

def student_logout(request):
    if 'sid' in request.session:
        del request.session['sid']
    context= {
        'error':'Logout Successfully.',
        'status':True
    }
    return render(request, 'student_login.html',context)

def admin_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = make_password(request.POST['password'],salt='101')
        email = request.POST['email']
        phone_no = request.POST['phone_no']

        adm_obj= Librarian.objects.filter(email=email)
        if len(adm_obj) != 0:
            context = {
                'error': 'Email was alreadry used',
                'status':True
            }
            return render(request, 'admin_signup.html', context)
        
        adm_obj= Librarian.objects.all().order_by('-uid')[:1]
        if len(adm_obj) != 0:
            uid=adm_obj[0].uid + 1
        else:
            uid=1
        
        Librarian.objects.create(
            uid=uid,
            name = name,
            password = password,
            email = email,
            phone_no = phone_no,
        )
        adm_obj = Librarian.objects.filter(email=email)
        context={
            'status':False,
            'info':'Your student_id is: '+str(adm_obj[0].uid),
            'test':password,
        }
        return render(request, 'signup_comp.html',context)
    
    return render(request, 'admin_signup.html')

def admin_login(request):
    if 'uid' in request.session:
        return redirect(adm_dashboard)
    
    if request.method == 'POST':
        uid = int(request.POST['uid'])
        password = request.POST['password']
        try:
            adm_obj = Librarian.objects.get(uid=uid)
            print(check_password(password, adm_obj.password))
            if check_password(password, adm_obj.password):
                request.session['uid'] = adm_obj.uid
                return redirect(adm_dashboard)
                
            else:
                context= {
                    'error':'User id or password is wrong1',
                    'status':True
                }
                return render(request, 'admin_login.html',context)
        except:
            context= {
                'error':'user id or password is wrong0',
                'status':True
            }
            return render(request, 'admin_login.html',context)

    return render(request, 'admin_login.html')

def admin_logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    context= {
                    'error':'Logout Successfully.',
                    'status':True
                }
    return render(request, 'admin_login.html', context)

def stds_verifiy(request):

    if not 'uid' in request.session:
        return redirect(admin_login)
    
    stds = Student.objects.filter(checked = False)
    context={
        'stds':stds
    }
    return render(request, 'stds_verifiy.html',context)

def std_verifiy(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    
    if 'checked' in request.GET and'sid' in request.GET:
        std_obj = Student.objects.get(sid=request.GET['sid'])
        if request.GET['checked'] == '1':
            std_obj.checked = True
            std_obj.active = True
            std_obj.checked_by = request.session['uid']
            std_obj.save()
        elif request.GET['checked'] == '2':
            std_obj.checked = True
            std_obj.active = False
            std_obj.checked_by = request.session['uid']
            std_obj.save()

    elif 'sid' in request.GET:
        std_objs = Student.objects.filter(sid=request.GET['sid'])
        context={
            'std':std_objs[0]
        }
        return render(request, 'std_verifiy.html', context)
    return redirect(stds_verifiy)

def adm_dashboard(request):
    if not 'uid' in request.session:
        context= {
                'error':'Your account is not login.',
                'status':True,
                
            }
        return render(request, 'admin_login.html', context)
    
    adm_obj = Librarian.objects.get(uid=request.session['uid'])
    return render(request, 'adm_dashboard.html',{'name': adm_obj.name})

def std_dashboard(request):
    if not 'sid' in request.session:
        
        context= {
                'error':'Your account is not login.',
                'status':True,
                
            }
        return render(request, 'student_login.html', context)
    
    std_obj = Student.objects.get(sid=request.session['sid'])
    return render(request, 'std_dashboard.html',{'name': std_obj.name})

def index(request):
    return render(request, 'home.html')