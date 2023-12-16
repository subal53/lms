from django.shortcuts import render,redirect
from bookapp.models import *
from account.views import admin_login,student_login
import datetime

# Create your views here.
def addNewBook(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    
    if request.method == 'POST':
        title = request.POST['title']
        auther = request.POST['auther']
        short_desc = request.POST['short_desc']
        quantity = request.POST['quantity']
        book_obj= Book.objects.all().order_by('-bid')[:1]
        if len(book_obj) != 0:
            bid=book_obj[0].bid + 1
        else:
            bid=1

        Book.objects.create(
            bid=bid,
            title = title,
            author = auther,
            short_desc = short_desc,
            quantity = quantity,
        )
        context = {
            'info':'New book '+title+' added('+quantity+')',
            'title':'New Book Add',
            'home':'adm_dashbord'
        }

        return render(request, 'post_screen.html',context )
    book_objs = Book.objects.all()
    context = {
        'books':book_objs
    }
    return render(request, 'add_new_book.html',context)

def addOldBook(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    
    try:
        if request.method == 'POST':
            addqunt = request.POST['addqunt']
            bid = request.POST['bid']

            book_obj =Book.objects.get(bid=bid)
            book_obj.add(int(addqunt))
            book_obj.save()

            context = {
                'info':'update book quntity(total = '+str(book_obj.quantity)+')',
                'title':'old Book Add',
                'home':'adm_dashbord'
            }

            return render(request, 'post_screen.html',context )

        
        if 'bid' in request.GET:
            bid = request.GET['bid']
            book_obj = Book.objects.get(bid=bid)
            context={
                'book':book_obj
            }

            return render(request, 'add_old_book.html', context)
        
    except:
        pass
    
    
    book_objs = Book.objects.all()
    context = {
        'books':book_objs
    }
    return render(request, 'add_new_book.html',context)

def searchBook(request):
    if not ('uid' in request.session or 'sid' in request.session):
        return redirect(student_login)
    
    try:
        if request.method == 'POST':
            search = request.POST['search']

            book_obj_title = Book.objects.filter(title__icontains = search).values()
            book_obj_bid = Book.objects.filter(bid__icontains = search).values()
            book_obj_author = Book.objects.filter(author__icontains = search).values()
            book_obj_short = Book.objects.filter(short_desc__icontains = search).values()

            book_objs = (book_obj_title | book_obj_author | book_obj_short | book_obj_bid).distinct()

            context = {
                'books': book_objs,
            }
            
        else:
            book_objs = Book.objects.all().values()

            context = {
                'books': book_objs
            }

        if 'sid' in request.session:
            context['student'] = True
        else:
            context['student'] = False
        
    except:
        context = {}
    
    return render(request, 'book_search.html',context)

def book_request(request):
    if 'bid' in request.GET and 'sid' in request.session:
        bid = request.GET['bid']
        sid = request.session['sid']
        date = datetime.datetime.now()
        
        book_obj = Book.objects.get(bid=bid) 
        issue_req = issue.objects.filter(sid=sid, actions = 0)
        issued = issue.objects.filter(sid=sid, actions = 1)
        issue_book = (issue_req | issued).distinct()
        
        for obj in issue_book:
            if obj.bid == bid:
                context = {
                    'info':'You alredy issued one copy of this book',
                    'title':'Book Request',
                    'home':'std_dashbord'
                }
                return render(request, 'post_screen.html',context )
        
        if book_obj.quantity > 0:
            if issue_book.count() < 2:
                
                issue.objects.create(
                    bid=bid,
                    sid=sid,
                    req_date = date,
                )
                book_obj.req()
                book_obj.save()

                context = {
                    'info':'Request Successfully',
                    'title':'Book Request',
                    'home':'std_dashbord'
                }
                return render(request, 'post_screen.html',context )
            else:
                context = {
                    'info':'Your have max request',
                    'title':'Book Request',
                    'home':'std_dashbord'
                }
                return render(request, 'post_screen.html',context )
        else:
            context = {
                    'info':'Book not availabe',
                    'title':'Book Request',
                    'home':'std_dashbord'
                }
            return render(request, 'post_screen.html',context )
        
    return redirect(searchBook)

def history(request):
    if not 'sid' in request.session:
        return redirect(student_login)
    else:
    
        sid = request.session['sid']
        issue_obj = issue.objects.filter(sid=sid).order_by('-id')
        data_pkg = []
        for obj in issue_obj:
            book_obj = Book.objects.get(bid=obj.bid)
            

            temp_pkg = {
                'title': book_obj.title,
                'author':book_obj.author,
                'req_date':obj.req_date,
                'issue_date':obj.issue_date,
                'return_date':obj.return_date,
                'close_date':obj.close_date,
                'status':obj.actions
            }
            if obj.actions == '1' or obj.actions == '2' :
                now_date = datetime.datetime.now()
                ret_date = obj.return_date
                day = ret_date-now_date.date()
                diff = day.days
            else:
                diff = 0

            if diff >=0:
                temp_pkg['color'] = "green"
            else:
                temp_pkg['color'] = "red"

            if obj.uid == None:
                temp_pkg['adm'] = '---'
            else:
                adm_obj = Librarian.objects.get(uid=obj.uid)
                temp_pkg['adm'] = adm_obj.name

            data_pkg += [temp_pkg]

        return render(request, 'history.html',{'obj':data_pkg})
    
def req_all(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    else:
    
        issue_obj = issue.objects.filter(actions=0)

        data_pkg = []
        for obj in issue_obj:
            book_obj = Book.objects.get(bid=obj.bid)
            std_obj = Student.objects.get(sid=obj.sid)
            temp_pkg = {
                'sid':std_obj.sid,
                'sname': std_obj.name,
                'roll':std_obj.roll,
                'id':obj.id,
                'title': book_obj.title,
                'author':book_obj.author,
                'req_date':obj.req_date,
            }

            data_pkg += [temp_pkg]

        return render(request, 'req_all.html',{'objs':data_pkg})
    
def issued(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    else:
        if 'id' in request.GET:
            id=request.GET['id']
            issue_obj = issue.objects.get(id=id)
            std_obj = Student.objects.get(sid=issue_obj.sid)
            book_obj = Book.objects.get(bid=issue_obj.bid)
            context={
                'id':id,
                'sname':std_obj.name,
                'roll':std_obj.roll,
                'dept':std_obj.dept,
                'title': book_obj.title,
                'author':book_obj.author,
                'req_date':issue_obj.req_date,
                'byId':True
            }

    
            return render(request,'issued.html',context)

        if 'id' in request.POST and 'ret_date' in request.POST and 'actions' in request.POST:
            id=request.POST['id']
            date=request.POST['ret_date']
            ret_date=datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))
            is_date=datetime.datetime.now()
            actions=request.POST['actions']

            issue_obj = issue.objects.get(id=id)
            
            if issue_obj.actions == '0':
                issue_obj.issue_date = is_date
                issue_obj.return_date = ret_date
                issue_obj.actions = int(actions)
                issue_obj.uid = request.session['uid']
                issue_obj.save()
            return redirect(req_all)
        
        if 'sid' in request.POST and 'bid' in request.POST and 'ret_date' in request.POST:
            print('test')
            now_date = datetime.datetime.now()
            bid=request.POST['bid']
            sid=request.POST['sid']
            date=request.POST['ret_date']
            ret_date=datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))
            book_obj = Book.objects.get(bid =bid)
            if book_obj.quantity >0:

                book_obj.req()
                issue.objects.create(
                    sid=sid,
                    bid=bid,
                    req_date=now_date,
                    issue_date=now_date,
                    return_date=ret_date,
                    uid=request.session['uid'],
                    actions=1,
                )
                book_obj.save()
            return redirect(req_all)

        context={
            'byId':False
        }
            
        return render(request,'issued.html',context)
    
def all_issued(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    
    if 'sid' in request.GET:
        issue_obj = issue.objects.filter(actions=1,sid=request.GET['sid'])
    else:
        issue_obj = issue.objects.filter(actions=1)

    data_pkg = []
    for obj in issue_obj:
        book_obj = Book.objects.get(bid=obj.bid)
        std_obj = Student.objects.get(sid=obj.sid)
        now_date = datetime.datetime.now()
        ret_date = obj.return_date
        day = ret_date-now_date.date()

        temp_pkg = {
            'sid':std_obj.sid,
            'sname': std_obj.name,
            'roll':std_obj.roll,
            'dept':std_obj.dept,
            'id':obj.id,
            'title': book_obj.title,
            'author':book_obj.author,
            'req_date':obj.req_date,
            'iss_date':obj.issue_date,
            'ret_date':obj.return_date,
            'day': day.days
        }

        if day.days >=0:
            temp_pkg['color'] = "green"
        else:
            temp_pkg['color'] = "red"

        data_pkg += [temp_pkg]

    return render(request, 'all_issued.html', {'objs':data_pkg})

def close(request):
    if not 'uid' in request.session:
        return redirect(admin_login)
    
    if 'id' in request.GET:
        id=request.GET['id']
        issue_obj = issue.objects.get(id=id)
        book_obj = Book.objects.get(bid=issue_obj.bid)
        book_obj.close()
        book_obj.save()

        issue_obj.actions=2
        issue_obj.close_date=datetime.datetime.now()
        issue_obj.save()
    return redirect(all_issued)