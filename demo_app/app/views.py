from django.shortcuts import render
from .models import xss,ccpa
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