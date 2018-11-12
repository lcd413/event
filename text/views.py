from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from text.models import Event,Guest
from django.contrib.auth.decorators import login_required
from utils.pager import Pagination
from django.forms import ModelForm
# Create your views here.
#登录
def login_action(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = auth.authenticate(username = username,password=password)
        if user is not None:
        # if username == "root" and password == "123":
            response = redirect("/event_manage/")
            request.session["user"]=username
            # response.set_cookie("user",username,3600)
            return response
        else:
            return render(request,"index.html",{"error":"username or password error!"})
    else:
        return  render(request,"index.html")

class EventModelForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        labels = {
            "name": "发布会名称",
            "limit": "参加人数",
            "status": "状态",
            "address": "地址",
            "start_time": "时间",
        }
class GuestModelForm(ModelForm):
    class Meta:
        model = Guest
        fields = "__all__"
        labels = {
            "realname": "名称",
            "phone": "手机",
            "email": "邮箱",
            "sign": "签到",
            "event": "发布会",
        }
#发布会编辑
def event_edit(request,nid):
    obj= Event.objects.filter(id=nid).first()
    if request.method=="GET":
        username = request.session.get("user")
        form_list =EventModelForm(instance=obj)
        return render(request,"event_manage_edit.html",{'user': username,"form":form_list})
    else:
        form_list = EventModelForm(request.POST,instance=obj)
        if form_list.is_valid():
            form_list.save()
            return redirect("/event_manage/")
#嘉宾编辑
def guest_edit(request,nid):
    obj=Guest.objects.filter(id=nid).first()
    if request.method == "GET":
        username = request.session.get("user")
        form_list= GuestModelForm(instance=obj)
        return render(request,"guest_manage_edit.html",{'user': username,"form":form_list})
    else:
        form_list = EventModelForm(request.POST,instance=obj)
        if form_list.is_valid():
            form_list.save()
            return redirect("/guest_manage/")
#发布会删除
def event_del(request,nid):
    Event.objects.filter(id=nid).delete()
    return redirect("/event_manage/")
def guest_del(request,nid):
    Guest.objects.filter(id=nid).delete()
    return redirect("/guest_manage/")
#发布会添加
def event_add(request):
    if request.method == "GET":
        username = request.session.get("user")
        form_list= EventModelForm()
        return render(request,"event_add.html",{'user': username,"form":form_list})
    else:
        form_list=EventModelForm(request.POST)
        if form_list.is_valid():
            form_list.save()
            return redirect("/event_manage/")
#嘉宾添加
def guest_add(request):
    if request.method =="GET":
        username= request.session.get("user")
        form_list =GuestModelForm()
        return render(request,"guest_add.html",{"user":username,"form":form_list})
    else:
        form_list = GuestModelForm(request.POST)
        if form_list.is_valid():
            form_list.save()
            return redirect("/guest_manage/")


#发布会列表页
def event_manage(request):
    eventinfor_list= Event.objects.all().count()
    EVENT_LIST= Event.objects.all()
    username = request.session.get("user")
    pager_obj = Pagination(request.GET.get('page', 1), eventinfor_list, request.path_info, request.GET)
    event_list = EVENT_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request, 'event_manage.html', {'user': username,"events":event_list,"page_html": html})

#嘉宾列表页
def guest_manage(request):
    guestinfor_list= Guest.objects.all().count()
    GUEST_LIST= Guest.objects.all()
    username = request.session.get("user")
    pager_obj = Pagination(request.GET.get('page', 1), guestinfor_list, request.path_info, request.GET)
    guest_list = GUEST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request, 'guest_manage.html', {'user': username,"guests":guest_list,"page_html": html})
#发布会搜索框
def search_name(request):
    username=request.session.get("user")
    search_name=request.GET.get("name")
    event_list=Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})
#嘉宾删除

#退出功能
def logout(request):
    return redirect("/login_action/")