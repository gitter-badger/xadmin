import datetime

from django.shortcuts import render
from .models import xss,ccpa,treatment,provider
# Create your views here.
from django.http import HttpResponse, Http404

def index(request):
    return HttpResponse("不要说话")

def detail(request,num,num2):
    return HttpResponse("detail-%s-%s"%(num,num2))


def printLogin(request):

    print('request',request)
    if request.method == "POST":
        name = request.POST.get('name')
        icc = request.POST.get('icc')
        card_no = request.POST.get('card_no')
        qry = xss.objects.filter(name=name,icc=icc,status='通过')
        print('qry',qry)
        for q in qry:
            if q.card_no == card_no:
                return render(request, 'print_card.html', {"qry": q,'verbose_name':'薪税师项目'})


        qry = ccpa.objects.filter(name=name,icc=icc,status='通过')
        print('qry',qry)
        for q in qry:
            if q.card_no == card_no:
                kskm = q.kskm.all()
                return render(request, 'print_card.html', {"qry": q,'verbose_name':'CCPA项目','kskm':kskm})

        return render(request, 'stulogin.html', {"error": '无信息，请核实'})

    else:
        return render(request, 'stulogin.html')
        #testResult_surnfu

    # qry = xss.objects.all()
    # print('qry',qry,request)
    # return render(request, 'stulogin.html', {"qry": qry})
def printLogin1(request,tid):

    print('request',request,tid)
    q = treatment.objects.get(id=tid)
    return render(request, 'print_card1.html', {"qry": q,'verbose_name':'薪税师项目'})
    return HttpResponse(int(tid))
    if request.method == "POST":
        name = request.POST.get('name')
        icc = request.POST.get('icc')
        card_no = request.POST.get('card_no')
        qry = xss.objects.filter(name=name,icc=icc,status='通过')
        print('qry',qry)
        for q in qry:
            if q.card_no == card_no:
                return render(request, 'print_card.html', {"qry": q,'verbose_name':'薪税师项目'})


        qry = ccpa.objects.filter(name=name,icc=icc,status='通过')
        print('qry',qry)
        for q in qry:
            if q.card_no == card_no:
                kskm = q.kskm.all()
                return render(request, 'print_card.html', {"qry": q,'verbose_name':'CCPA项目','kskm':kskm})

        return render(request, 'stulogin.html', {"error": '无信息，请核实'})

    else:
        return render(request, 'stulogin.html')
        #testResult_surnfu

    # qry = xss.objects.all()
    # print('qry',qry,request)
    # return render(request, 'stulogin.html', {"qry": qry})
def printLogin2(request,tid):
    print('request',request,tid)
    p = provider.objects.get(id=tid)
    cur_time = datetime.datetime.now()  # 如果数据库保存的是UTC时间,程序不会蹦但是会提示你这不是本地时间
    # 当前天 显示当前日期是本周第几天
    day_num = cur_time.isoweekday()
    # 计算当前日期所在周一
    monday = (cur_time - datetime.timedelta(days=day_num))
    import time
    strTime =  monday.strftime("%Y-%m-%d")
    endTime =  cur_time.strftime("%d/%m/%Y %H:%M:%S")
    beginTime =  monday.strftime("%d/%m/%Y"+' 00:00:00')
    print('11strTime',strTime)
    print('monday',monday,'cur_time',cur_time)
    # 查询一周内的数据
    # all_datas = YourModel.objects.filter(time__range=(cur_time, monday))
    # query_set = treatment.objects.extra(select={'count': 'count(1)'},
    #                                     order_by=['-count']).values('count', 'prov')
    q = treatment.objects.filter(date__gte=strTime).all()# .values_list('prov')annotate(num=Count('id')).
    # q = treatment.objects.raw('select prov_id,count(1) from app_treatment where date>'+strTime+' group by prov_id')
    print('q',q)
    relist = []
    for i in q:
        # j = i.prov.objects
        hasflag = 0
        for j in relist:
            if i.prov.fullname()==j['name']:
                j['num']=j['num']+1
                hasflag = 1
                break
        if hasflag==0:
            pnum = {'name': i.prov.fullname(), 'num': 1}
            relist.append(pnum)
    print('relist',relist)
    return render(request, 'print_card2.html', {"qry": relist,'beginTime':beginTime,'endTime':endTime})