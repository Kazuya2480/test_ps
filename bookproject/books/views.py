from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.utils import timezone
from django.views.generic import(
   View, ListView, DetailView
) 
from django.urls import reverse
import os
from django.db.models import Q, Avg
from django.contrib import messages
import time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'books/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'books/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'books/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'books/adminsignup.html',{'form':form})

def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'books/studentsignup.html',context=mydict)



def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'books/adminafterlogin.html')
    else:
        return render(request,'books/studentafterlogin.html')
    
def afterlogin_view2(request, id):
    if is_admin(request.user):
        return render(request,'books/adminafterlogin.html')
    else:
        return render(request,'books/studentafterlogin.html')

def error_404page(request, expection):
    return render(request, 'books/404.html', status=404)

def error_500page(request): # 以下追記箇所
    return render(request, 'books/500.html', status=500)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin) #change
def addbook_view(request):
    form=forms.BookForm(label_suffix="")
    if request.method == "POST":
        isbn = request.POST["isbn"]
        name = request.POST["name"]
        publisher = request.POST["publisher"]
        author = request.POST["author"]
        category = request.POST["category"]
        publisheddate = request.POST["publisheddate"]
        image =request.FILES.get("image")
        version = request.POST["version"]
        place = request.POST["place"]
        obj=models.Book(isbn=isbn, name=name, publisher=publisher, category=category,
                        author=author, publisheddate=publisheddate, image=image, 
                        version=version, place=place)
        obj.save()
    
        return render(request,'books/bookadded.html', )
       
        
    return render(request,'books/addbook.html',{'form':form})
    


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)#change
def viewbook_view(request):
    books=models.Book.objects.all()
    keyword = request.GET.get('keyword')
    t = request.GET.get('t')

    if keyword:
        books = books.filter(
            Q(name__icontains=keyword)|Q(author__icontains=keyword)|Q(publisher__icontains=keyword)|Q(isbn__icontains=keyword)
        )
    else:
        books = books.all()
    if t:
        books = books.filter(
            Q(category__icontains=t)
        )
    else:
        books = books.all()
    return render(request,'books/viewbook.html',{'books':books})

@login_required(login_url='studentlogin')
def deleteviewbook(request, id):
    obj = get_object_or_404(models.Book, id=id)
    if request.POST:
        obj.delete()
        return redirect("viewbook")
    return render(request, 'books/deleteviewbook.html', {'obj':obj})

@login_required(login_url='studentlogin')
def issuebook_confirm(request, id):
    book = models.Book.objects.filter(id=id)
    return render(request, 'books/bookissueconfirm.html', {'book':book})

@login_required(login_url='studentlogin') #change
def issuebook_finish(request, id):
    user=request.user
    book=models.Book.objects.filter(id=id)
    gen = models.StudentExtra.objects.filter(user_id=user.id)
    obj = models.IssuedBook()
     
    for book in book:
      for gen in gen:
         obj.isbn=book.isbn
      obj.enrollment=gen.enrollment
      obj.save()
      history=models.BookHistory.objects.create(
        user=user,
        book=book
      )
     
    return render(request, 'books/bookissuedfinish.html',{'book':[book], },)
        
@login_required(login_url='studentlogin')
def bookhistory(request):
    user = request.user.id
    historybook=models.BookHistory.objects.filter(user=user).order_by('-id')
    pagenator = Paginator(historybook, 6)
    page = request.GET.get('page', 1)
    try:
        pages = pagenator.page(page)
    except PageNotAnInteger:
        pages = pagenator.page(1)
    except EmptyPage:
        pages = pagenator.page(1)
    return render(request, 'books/bookhistory.html', {'pages':pages})

@login_required(login_url='studentlogin')
def bookhistory2(request, id):
    user = request.user.id
    historybook=models.BookHistory.objects.filter(user=user).order_by('-id')
    pagenator = Paginator(historybook, 6)
    page = request.GET.get('page', 1)
    try:
        pages = pagenator.page(page)
    except PageNotAnInteger:
        pages = pagenator.page(1)
    except EmptyPage:
        pages = pagenator.page(1)
    return render(request, 'books/bookhistory.html', {'pages':pages})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin) #ppp
def viewissuedbook_view(request):
    user=request.user
    enr=models.StudentExtra.objects.filter(user=user)
    issuedbooks=models.IssuedBook.objects.all()
    
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.year)+'年'+str(ib.issuedate.month)+'月'+str(ib.issuedate.day)+'日'
        expdate=str(ib.expirydate.year)+'年'+str(ib.expirydate.month)+'月'+str(ib.expirydate.day)+'日'
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,books[i].isbn,issdate,expdate,fine)
            i=i+1
            li.append(t)
            
   

    return render(request,'books/viewissuedbook.html',{'li':li })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deleteissuedbook(request, isbn):
    obj = models.IssuedBook.objects.filter(isbn=isbn) #修正
    if request.POST:
        obj.delete()
        return redirect("viewissuedbook")
    return render(request, 'books/deleteissuedbook.html', {'obj':obj})

@login_required(login_url='studentlogin')
def deleteissuedbook_student(request, isbn):
    obj = models.IssuedBook.objects.filter(isbn=isbn) #修正
    if request.POST:
        obj.delete()
        return redirect("viewissuedbookbystudent")
    return render(request, 'books/deleteissuedbookbystudent.html', {'obj':obj})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewreservebook_view(request):
    reservebook = models.CartItems.objects.all()
    return render(request, 'books/viewreservebook_view.html', {'reservebook':reservebook})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.order_by('id')
    keyword = request.GET.get('keyword')

    if keyword:
        students = students.filter(
            Q(enrollment__icontains=keyword)
        )
    else:
        students = students.all()

    return render(request,'books/viewstudent.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view_delete(request, pk):
    obj = get_object_or_404(models.StudentExtra, pk=pk)
    if request.POST:
        obj.delete()
        return redirect("viewstudent")
    return render(request, 'books/viewstudent_delete.html', {'obj':obj})


# -------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)
    datetime_1 = datetime.now()  # datetime.datetime型とdatetime.date型で比較するとエラーが発生する
    date_1 = datetime_1.date()  # IssueBookのexpirydateはdatetime.date型なのでdate_1でdatetime.date型に変換する必要がある
    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,book.name,book.author,book.isbn,book.place)
            li1.append(t)
        issdate=str(ib.issuedate.year)+'年'+str(ib.issuedate.month)+'月'+str(ib.issuedate.day)+'日'
        expdate=str(ib.expirydate.year)+'年'+str(ib.expirydate.month)+'月'+str(ib.expirydate.day)+'日'
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)
        # bb = date_1 + timedelta(days=14)
        limit_1 = ib.expirydate - timedelta(days=1)
        limit_2 = ib.expirydate - timedelta(days=2)
        if ib.expirydate < date_1: # ib.expirydate(返却期限日)がdate_1(今日)より小さければTrue(message発生)
            messages.add_message(request, messages.ERROR, '返却期限が過ぎています')
        if ib.expirydate == date_1:
            messages.add_message(request, messages.ERROR, '返却期限日が迫っています')
        if limit_1 == date_1:
            messages.add_message(request, messages.ERROR, '返却期限日が迫っています')
        if limit_2 == date_1:
            messages.add_message(request, messages.ERROR, '返却期限日が迫っています')
       # print(bb)
       # print(limit_1)
       # print(limit_2)
    return render(request,'books/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

@login_required(login_url='studentlogin')
def viewissuedbookbystudent2(request, id):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)
    datetime_1 = datetime.now()  # datetime.datetime型とdatetime.date型で比較するとエラーが発生する
    date_1 = datetime_1.date()  # IssueBookのexpirydateはdatetime.date型なのでdate_1でdatetime.date型に変換する必要がある
    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,book.name,book.author,book.isbn,book.place)
            li1.append(t)
        issdate=str(ib.issuedate.year)+'年'+str(ib.issuedate.month)+'月'+str(ib.issuedate.day)+'日'
        expdate=str(ib.expirydate.year)+'年'+str(ib.expirydate.month)+'月'+str(ib.expirydate.day)+'日'
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)
        # bb = date_1 + timedelta(days=17)
        limit_1 = ib.expirydate - timedelta(days=1)
        limit_2 = ib.expirydate - timedelta(days=2)
        

        if ib.expirydate < date_1: # ib.expirydate(返却期限日)がdate_1(今日)より小さければTrue(message発生)
            messages.add_message(request, messages.ERROR, '返却期限が過ぎています')
        if ib.expirydate == date_1:
            messages.add_message(request, messages.ERROR, '返却期限日が迫っています')
        if limit_1 == date_1:
            messages.add_message(request, messages.ERROR, '返却期限日が迫っています')
        if limit_2 == date_1:
            messages.add_message(request, messages.ERROR, '返却期限日が迫っています')
       # print(bb)
       # print(limit_1)
       # print(limit_2)
      
    return render(request,'books/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def aboutus_view(request):
    return render(request,'books/aboutus.html')



@login_required(login_url='studentlogin')
def search(request):
    book_search = models.Book.objects.order_by('-id')
    keyword = request.GET.get('keyword')
    t = request.GET.get('t')
    if keyword:
            book_search = book_search.filter(
              Q(isbn__icontains=keyword)| Q(name__icontains=keyword)| Q(author__icontains=keyword) | Q(publisher__icontains=keyword) 
            )
            messages.success(request,'「{}」検索結果', format(keyword))
    else:
        book_search = book_search.all()
    if t:
        book_search = book_search.filter(
              Q(category__icontains=t)
        )
    else:
        book_search = book_search.all()
    return render(request, 'books/book_search.html', {'book_search':book_search})

@login_required(login_url='studentlogin')
def search2(request, id):
    book_search = models.Book.objects.order_by('-id')
    keyword = request.GET.get('keyword')
    t = request.GET.get('t')
    if keyword:
            book_search = book_search.filter(
              Q(isbn__icontains=keyword)| Q(name__icontains=keyword)| Q(author__icontains=keyword) | Q(publisher__icontains=keyword) 
            )
            messages.success(request,'「{}」検索結果', format(keyword))
    else:
        book_search = book_search.all()
    if t:
        book_search = book_search.filter(
              Q(category__icontains=t)
        )
    else:
        book_search = book_search.all()
    return render(request, 'books/book_search.html', {'book_search':book_search})

@login_required(login_url='studentlogin')
def detail(request, **kwargs):
    book = models.Book.objects.get(pk=kwargs['id'])
    rent = models.IssuedBook.objects.filter(isbn=book.isbn)
    is_added = models.CartItems.objects.filter(
        cart_id = request.user.id,
        id = kwargs.get('id'),
        book_isbn = book.isbn
    ).first
    reserved = models.CartItems.objects.filter(book_isbn=book.isbn)
    reserveuser = models.CartItems.objects.filter(cart_id=request.user.id)
    if request.method == 'POST':
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content','')
        redirect_url = reverse('detail')
        review = models.BookReview.objects.create(book=book, user=request.user, stars=stars, content=content)
        url = f'{redirect_url}{book.id}'
        return redirect(url)
    post_review = models.BookReview.objects.order_by('data_added').reverse()
    pagenator = Paginator(post_review, 7)
    page = request.GET.get('page', 1)
    try:
        pages = pagenator.page(page)
    except PageNotAnInteger:
        pages = pagenator.page(1)
    except EmptyPage:
        pages = pagenator.page(1)
    return render(request, 'books/book_detail.html', context={
        'book':book, 'rent':rent, 'is_added':is_added, 'pages':pages, 'reserved':reserved, 
        'reserveuser':reserveuser
        })










def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url='studentlogin')
def add_book(request):
    if is_ajax(request=request):
        book_id = request.POST.get('id') 
        book_isbn = request.POST.get('isbn') 
        cart = models.Carts.objects.get_or_create(
            user=request.user
        )
        if all([book_id, book_isbn, cart,]):
            models.CartItems.objects.save_item(
               book_id=book_id,
               book_isbn=book_isbn,
               cart=cart[0]
            )
            return JsonResponse({'message': '書籍を予約一覧に追加しました'})
    return render(request, 'books/book_detail.html')
 

@login_required(login_url='studentlogin')
def reserveviewbyuser(request):
    user_id = request.user.id
    query = models.CartItems.objects.filter(cart_id=user_id)
    items = []
    for item in query.all():
        picture = item.book.image
        picture = picture if picture else None
        tmp_item = {
            'picture': picture,
            'name': item.book.name,
            'author': item.book.author,
            'publisher': item.book.publisher,
            'date': item.date,
            'id': item.id,
        }
        items.append(tmp_item)
    return render(request, 'books/reserveviewbyuser.html',{'items': items })

@login_required(login_url='studentlogin')
def reserveviewbyuser2(request, id):
    user_id = request.user.id
    query = models.CartItems.objects.filter(cart_id=user_id)
    items = []
    for item in query.all():
        picture = item.book.image
        picture = picture if picture else None
        tmp_item = {
            'picture': picture,
            'name': item.book.name,
            'author': item.book.author,
            'publisher': item.book.publisher,
            'date': item.date,
            'id': item.id,
        }
        items.append(tmp_item)
    return render(request, 'books/reserveviewbyuser.html',{'items': items })


@login_required(login_url='studentlogin')
def reservedeleteviewbyuser(request, pk):
    obj = get_object_or_404(models.CartItems, pk=pk)
    if request.POST:
        obj.delete()
        return redirect("reserveviewbyuser")
    return render(request, 'books/reservebook_delete.html', {'obj':obj})


