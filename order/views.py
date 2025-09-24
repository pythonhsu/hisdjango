from django.shortcuts import render,redirect
from order.models import Product,UserInfo,Member,OrderDetail
from order.forms import UserInfoForm,MemberForm,MemberLogin,ProductSearchForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.urls import reverse



# Create your views here.
def index(request):
    status=request.session.get('is_login')
    uname=request.session.get('uname')
    return render(request,'index.html',locals())


def products(request):
    product=Product.objects.all()
    return render(request,'products.html',locals())

#註冊
def signup(request):
    if request.method == "POST":
        form=UserInfoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/signupok')
            except:
                pass
    else:
        form=UserInfoForm()
    return render(request,'signup.html',{'form':form})

def signupok(request):
    userinfo=UserInfo.objects.all()
    return render(request,'signupok.html',{'userinfo':userinfo})


# #會員註冊, 方法一
# def register(request):  
#     member=Member.objects.all()
#     form=MemberForm(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             try:
#                 form.save()
#                 request.session['is_login']=True
#                 request.session['email']=form.cleaned_data['email']
#                 request.session['pwd']=form.cleaned_data['pwd']
#                 request.session['uname']=form.cleaned_data['uname']
#                 return redirect('/member')
#             except:
#                 pass
#                 return redirect('/register/')
#     else:
#         form=MemberForm()   #若請求的方法不是POST, 則建立空的表單實體    
#     context={
#         'member':member,
#         'form':form
#     }   
#     return render(request,'register.html',context)


#會員註冊, 方法二
# def register(request):  
#     member=Member.objects.all()
#     form=MemberForm(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             try:
#                 form.save()
#                 email=form.cleaned_data['email']
#                 result=Member.objects.get(email=email)
#                 request.session['is_login']=True
#                 request.session['email']=result.email
#                 request.session['pwd']=result.pwd
#                 request.session['uname']=result.uname                
#                 return redirect('/member')
#             except:
#                 pass
#                 return redirect('/register/')
#     else:
#         form=MemberForm()   #若請求的方法不是POST, 則建立空的表單實體    
#     context={
#         'member':member,
#         'form':form
#     }   
#     return render(request,'register.html',context)

#會員註冊, 方法三,密碼編碼,雜湊碼(hash code)
def register(request):
    if request.method == 'POST':
        form=MemberForm(request.POST)
        if form.is_valid():
            try:
                form.clean_password()   #直接調用,進行驗證                
                member=form.save(commit=False)  #建立member 實體,但不要馬上儲存到資料庫
                member.pwd= make_password(form.cleaned_data['pwd'])  #將密碼加密
                member.save()

                #將會員的資料存到 session
                request.session['is_login']=True
                request.session['email']=member.email
                request.session['uname']=member.uname
                request.session['pwd']=member.pwd  #密碼已經加密
                return redirect('/member')
            except Exception as e:
               print(f"Error: {e} ")
               return redirect('/register/')
    else:
        form=MemberForm() #如果請求方法不是POST, 則為空表單
    context={
        'form':form
    }
    return render(request, 'register.html' , context)        



#會員註冊,登入成功
def member(request):
    status=request.session.get('is_login')
    email=request.session.get('email')
    pwd=request.session.get('pwd')
    uname=request.session.get('uname') 
    if not status:
        return redirect('/')
    return render(request,'member.html',locals())

#會員登出
def logout(request):
    request.session.flush()
    return redirect('/')

#會員登入
# def login(request):
#     member=Member.objects.all()
#     form=MemberLogin(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             email=form.cleaned_data['email']
#             pwd=form.cleaned_data['pwd']
#             memberobj=Member.objects.filter(email=email,pwd=pwd).first()
#             if not memberobj:
#                 return redirect('/login')
#             else:
#                 request.session['is_login']=True
#                 request.session['email']=memberobj.email
#                 request.session['pwd']=memberobj.pwd
#                 request.session['uname']=memberobj.uname
#                 return redirect('/member')
#     else:
#         form=MemberLogin() 
#     context={
#         'member':member,
#         'form':form
#     }
#     return render(request,'login.html',context)

#會員登入, 密碼有編碼
def login(request):
    form=MemberLogin(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email=form.cleaned_data['email']
            pwd=form.cleaned_data['pwd']

            #依電子郵件找會員物件
            memberobj=Member.objects.filter(email=email).first()
            
            if not memberobj:   #無此會員
                return render(request,'login.html',{'form':form,'error': '無此帳號'})
            
            if check_password(pwd,memberobj.pwd):   #使用此函數,比較加密密碼和用戶輸入明文密碼
                request.session['is_login']=True
                request.session['email']=memberobj.email
                request.session['pwd']=memberobj.pwd
                request.session['uname']=memberobj.uname
                return redirect('/member')
            else:
                return render(request,'login.html',{'form':form,'error': '密碼錯誤'})
    context ={
        'form':form
    }
    return render(request,'login.html',context)

#會員更新
# def update(request,email):
#     status=request.session.get('is_login') 
#     #uname=request.session.get('uname')  #解決修改資料(update),staus 為 none 的問題，方法一：加上此行   
#     if status:
#         member=Member.objects.get(email=email)
#         form=MemberForm(instance=member)  #宣告一個實體,以請求的資料為參數,參數初始化表單,確保表單載入時包含了會員的資料
       
#        #處理POST 的請求,更新資料
#         if request.method == 'POST':
#             form=MemberForm(request.POST,instance=member)
#             if form.is_valid():
#                 try:
#                     form.save()
#                     request.session['is_login']=True
#                     request.session['email']=member.email
#                     request.session['pwd']=member.pwd
#                     request.session['uname']=member.uname
#                     return redirect('/updateok')
#                 except:
#                     pass   
#         context={
#             'member':member,
#             'form':form,
#             #'status':status, #解決修改資料(update),staus 為 none 的問題，方法一：
#             #'uname':uname,
#         }
#         return render(request,'update.html',context)
#     else:
#         return redirect('/')

#會員更新,有編號
def update(request,email):
    status=request.session.get('is_login') 
    #uname=request.session.get('uname')  #解決修改資料(update),staus 為 none 的問題，方法一：加上此行   
    if status:
        member=Member.objects.get(email=email)
        form=MemberForm(instance=member)  #宣告一個實體,以請求的資料為參數,參數初始化表單,確保表單載入時包含了會員的資料
       
       #處理POST 的請求,更新資料
        if request.method == 'POST':
            form=MemberForm(request.POST,instance=member)
            if form.is_valid():
                try:                    
                    form.clean_password() #儲存之前,先調用此函數進行密碼驗證
                    password=form.cleaned_data['pwd']
                    if password:  #若密碼有被修改                  
                        member.pwd=make_password(password) #將密碼加密
                    form.save()
                    request.session['is_login']=True
                    request.session['email']=member.email
                    request.session['pwd']=member.pwd
                    request.session['uname']=member.uname
                    return redirect('/updateok')
                except Exception as e:
                    print(f"Error: {e} ")
                    #return redirect('/')
                    #return redirect(f'/update/{member.email}')                       
                    return redirect(reverse('update',args=[email]))  #將email 參數傳給url
                    
        context={
            'member':member,
            'form':form,
            #'status':status, #解決修改資料(update),staus 為 none 的問題，方法一：
            #'uname':uname,
        }
        return render(request,'update.html',context)
    else:
        return redirect('/')
    
#更新會員資料OK
def updateok(request):
    status=request.session.get('is_login')
    email=request.session.get('email')
    pwd=request.session.get('pwd')
    uname=request.session.get('uname')
    if not status:
        return redirect('/')
    return render(request,'updateok.html',locals())


#刪除會員資料
def delete(request,email):
    status=request.session.get('is_login')
    if not status:
        return redirect('/')
    
    member=Member.objects.get(email=email)
    member.delete()
    logout(request)
    return render(request,'index.html',{'delflag':True})

# def product_order(request): 
#     #orders=None #先預設沒有訂單
#     orders=[]
#     OrderDetail.objects.none
#     form=ProductSearchForm()
#     if request.method == 'POST':
#         form=ProductSearchForm(request.POST)
#         if form.is_valid():
#             pid=form.cleaned_data['pid']
#             orders=OrderDetail.objects.filter(pid=pid)  #查詢與產品編號相關的訂單          
#     return render(request,'product_order.html',{'form':form,'orders':orders})


def product_order(request): 
    orders = []  # 預設沒有訂單   
    pname=''    #記錄產品名稱
    count=0 #訂單筆數
    form = ProductSearchForm()
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            pid = form.cleaned_data['pid']
            orders = OrderDetail.objects.filter(pid=pid)  # 查詢與產品編號相關的訂單   

            if orders.exists():
                pname=Product.objects.get(id=pid).name
                count=orders.count() 
            else:
                pname='沒有這個產品'
                count=0
    #return render(request, 'product_order.html', {'form': form, 'orders': orders})
    return render(request, 'product_order.html',locals())



