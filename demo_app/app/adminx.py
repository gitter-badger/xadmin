from __future__ import absolute_import

import xlrd
# from dateutil.relativedelta import relativedelta

import xadmin
from xadmin import views
from .models import IDC, Host, MaintainLog, HostGroup, AccessRecord,ccpa,xss,kmChoices,customer,treatment_item,fund,groupinfo,litreat,usergroupinfo
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
import datetime
import calendar
from django.db.models import Avg
import time
#
# @xadmin.sites.register(views.website.IndexView)
# class MainDashboard(object):
#     widgets = [
#         [
#             {"type": "html", "title": "琪睿登记系统",
#              "content": "<h3> 欢迎使用本系统! </h3><p>有问题联系客服: <br/>QQ  : 494514014</p>"},
#             {"type": "chart", "model": "app.accessrecord", "chart": "user_count",
#              "params": {"_p_date__gte": "2013-01-08", "p": 1, "_p_date__lt": "2013-01-29"}},
#             {"type": "list", "model": "app.host", "params": {"o": "-guarantee_date"}},
#         ],
#         [
#             {"type": "qbutton", "title": "Quick Start",
#              "btns": [{"model": Host}, {"model": IDC}, {"title": "Google", "url": "http://www.google.com"}]},
#             {"type": "addform", "model": MaintainLog},
#         ]
#     ]


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = False
    use_bootswatch = False
    # search_models = False


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    global_search_models = []
    # global_models_icon = {
    #     Host: "fa fa-laptop", IDC: "fa fa-cloud"
    # }
    menu_style = 'default'  # 'accordion'


class MaintainInline(object):
    model = MaintainLog
    extra = 1
    style = "accordion"



@xadmin.sites.register(groupinfo)
class groupinfoAdmin(object):
    list_display = ("group_no","group_name")
    list_display_links = ("group_name",)
    # wizard_form_list = [
    #     ("First's Form", ("name", "description")),
    #     ("Second Form", ("contact", "telphone", "address")),
    #     ("Thread Form", ("customer_id",))
    # ]
    search_fields = [ "group_name"]
    list_filter = [
        "group_name"
    ]
    list_quick_filter = [{"field": "group_name", "limit": 10}]

    search_fields = ["group_name"]
    # relfield_style = "fk-select"
    reversion_enable = True

    actions = [BatchChangeAction, ]
    batch_fields = ("group_name")



@xadmin.sites.register(litreat)
class litreatAdmin(object):
    list_display = [ "yearm","cust_name","icc_id","all_acc","avg_acc","is_life","jy_count","jy_num","day_avg","all_jy_count","all_jy_num","is_show","is_ontime",]
    list_x_display = ["is_life","jy_count","jy_num","day_avg","all_jy_count","all_jy_num","is_show","is_ontime", ]

    detailitem = ['all_acc']

    # show_detail_fields = ['all_acc']
    # grid_layouts  = ['yearm',]
    #"nowm_acc","open_ins","open_no","can_use_acc","used_acc","acc_detail","is_quit" "con_num",
    list_display_links = ("icc_id",)
    # wizard_form_list = [
    #     ("First's Form", ("name", "description")),
    #     ("Second Form", ("contact", "telphone", "address")),
    #     ("Thread Form", ("customer_id",))
    # ]
    search_fields = [ "yearm","icc_id","nowm_acc","all_acc","is_life","cust_name","con_num","open_ins","open_no","jy_count","jy_num","day_avg","all_jy_count","all_jy_num","is_show","is_ontime","can_use_acc","used_acc","acc_detail","is_quit"]
    list_filter = [
        "yearm","open_no"
    ]
    list_quick_filter = [{"field": "open_ins", "limit": 10}]
    # date_hierarchy = 'yearm'
    # search_fields = ["open_no"]
    reversion_enable = False
    list_export = ('xls',)
    list_export1 = ('xls',)
    # relfield_style = "fk-select"0.



    reversion_enable = True
    import_excel = True

    # actions = [BatchChangeAction, ]
    # batch_fields = ("open_no")

    def get_list_queryset(self):
        print('self.request', self.request)
        queryset = super().get_list_queryset()
        if self.user.is_superuser:
            return queryset
        print(self.user,'self.request.user',self.request.user)
        aa=usergroupinfo.objects.filter(userinfo=self.user).first()
        groupidlist =[]
        if aa and aa.group:
            print('aa',aa,aa.group.all())
            for a in aa.group.all():
                groupidlist.append(a.group_no)
        print('0queryset',queryset.values())
        queryset = queryset.filter(open_no__in=groupidlist)#.all().only('jy_count')
        # import copy
        # d = copy.deepcopy(queryset)  # 对象拷贝，深拷贝
        # print('1queryset', d.values())
        # for aa in d.values():
        #     print('aa',aa)
        #     for aaa in aa:
        #         print('aaa',aaa)
        #         if aaa =='jy_count':
        #             print('中财',aa[aaa])
        #             aa[aaa] = '*'
        #             print('中财1',aa[aaa])
        #
        #     print('1aa',aa)
        # print('1queryset', d.values())

        return queryset

    def post(self, request, *args, **kwargs):
        #  导入逻辑
        if 'excel' in request.FILES:
            print('excel',request.FILES,'month',request.POST.get('month'))
            opmonth = request.POST.get('month')
            wb = xlrd.open_workbook(
                filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
            table = wb.sheets()[0]
            row = table.nrows
            t1col = ['账号', '开户机构', '客户名', '身份证', '交易笔数', '交易金额']
            t1col2 = ['机构名称', '挂靠机构号', '法人名称', '法人身份证', '卡号', '日均', '交易总金额', '交易总笔数']
            t1col3 = ['身份证', '客户名', '百富生活圈折扣', '是否展示易拉宝', '是否按时还款', '是否清退', '本月消费积分', '积分消费详情','缴纳利息','投诉次数']
            tflag=0
            add_litreat_list = []
            op_icc_list=[]
            #获取账号归属机构列表
            print(self.user, 'self.request.user', self.request.user)

            groupidlist = []
            if not self.user.is_superuser:
                aa = usergroupinfo.objects.filter(userinfo=self.user).first()
                # print('aa', aa, aa.group.all())
                for a in aa.group.all():
                    groupidlist.append(a.group_no)
            # queryset = queryset.filter(open_no__in=groupidlist)
            for i in range(0, row):
                col = table.row_values(i)
                print('col',col)
                if i==0 and t1col==col:
                    print('是表一')
                    tflag=1
                elif i==0 and t1col2==col:
                    print('是表二')
                    tflag=2
                elif i==0 and t1col3==col:
                    print('是表三')
                    tflag=3

                if i>0:
                    if tflag==1:
                        #处理表1数据
                        op_icc_list.append(col[3])
                        aa = litreat.objects.filter(yearm=opmonth,icc_id=col[3])
                        print('aa',aa)
                        bb = groupinfo.objects.filter(group_no=col[1]).first()
                        if not bb:
                            obj = groupinfo(
                                group_no=col[1],
                                group_name=col[1],
                            )
                            obj.save()
                        #非超级管理员只能导入部分行的数据
                        if not self.user.is_superuser and col[1] not in groupidlist:
                            print(col[1],'col[1] not in groupidlist',groupidlist)
                            continue



                        if aa:
                            #有值更新
                            litreat.objects.filter(yearm=opmonth, icc_id=col[3]).update(
                                con_num=col[0],
                                open_no=col[1],
                                cust_name=col[2],
                                jy_count=col[4],
                                jy_num=col[5],
                            )
                        else:
                            #无值新增
                            obj = litreat(
                                yearm=opmonth,
                                icc_id=col[3],
                                con_num=col[0],
                                open_no=col[1],
                                cust_name=col[2],
                                jy_count=col[4],
                                jy_num=col[5],
                            )
                            add_litreat_list.append(obj)
                    if tflag==2:
                        #处理表1数据
                        op_icc_list.append(col[3])
                        aa = litreat.objects.filter(yearm=opmonth,icc_id=col[3])
                        bb = groupinfo.objects.filter(group_no=col[1]).first()
                        if not bb:
                            obj = groupinfo(
                                group_no=col[1],
                                group_name=col[0],
                            )
                            obj.save()
                        else:
                            groupinfo.objects.filter(group_no=col[1]).update(
                                group_name=col[0],
                            )
                        print('aa',aa)
                        if aa:
                            #有值更新
                            litreat.objects.filter(yearm=opmonth, icc_id=col[3]).update(
                                open_ins=col[0],
                                open_no=col[1],
                                cust_name=col[2],
                                day_avg=col[5],
                                all_jy_count=col[7],
                                all_jy_num=col[6],
                            )
                        else:
                            #无值新增
                            obj = litreat(
                                yearm=opmonth,
                                icc_id=col[3],
                                con_num=col[4],
                                open_ins=col[0],
                                open_no=col[1],
                                cust_name=col[2],
                                day_avg=col[5],
                                all_jy_count=col[7],
                                all_jy_num=col[6],
                            )
                            add_litreat_list.append(obj)
                            print('add_litreat_list',add_litreat_list)
                    if tflag==3:
                        #处理表1数据
                        op_icc_list.append(col[0])
                        aa = litreat.objects.filter(yearm=opmonth,icc_id=col[0])
                        print('aa',aa)
                        if aa:
                            #有值更新
                            litreat.objects.filter(yearm=opmonth, icc_id=col[0]).update(
                                is_life=col[2],
                                is_show=False if (col[3] == '否') else True,
                                is_ontime=False if (col[4] == '否') else True,
                                used_acc=col[6],
                                acc_detail=col[7],
                                jnlx_num=col[8],
                                is_quit=False if (col[5] == '否') else True,
                                ts_count=col[9],
                            )
                        else:
                            #无值新增
                            obj = litreat(
                                yearm=opmonth,
                                icc_id=col[0],
                                cust_name=col[1],
                                is_life=col[2],
                                is_show=False if(col[3]=='否')else True,
                                is_ontime=False if(col[4]=='否')else True,
                                used_acc=col[6],
                                acc_detail=col[7],
                                jnlx_num=col[8],
                                is_quit=False if(col[5]=='否')else True,
                                ts_count=col[9],
                            )
                            add_litreat_list.append(obj)
                            print('add_litreat_list',add_litreat_list)
            if add_litreat_list != []:
                litreat.objects.bulk_create(add_litreat_list)
            updatejf(opmonth,op_icc_list)
            pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
        # return super(litreatAdmin, self).post(request, *args, **kwargs)  # 此返回值必须是这样
        return super().post(request, *args, **kwargs)

# @xadmin.sites.register(litreat)
# class litreatAdmin(object):
#     list_display = [ "yearm","icc_id","cust_name","con_num","nowm_acc","all_acc","is_life","open_ins","open_no","jy_count","jy_num","day_avg","all_jy_count","all_jy_num","is_show","is_ontime","can_use_acc","used_acc","acc_detail","is_quit"]
#     list_display_links = ("icc_id",)
#     # wizard_form_list = [
#     #     ("First's Form", ("name", "description")),
#     #     ("Second Form", ("contact", "telphone", "address")),
#     #     ("Thread Form", ("customer_id",))
#     # ]
#     search_fields = [ "yearm","icc_id","nowm_acc","all_acc","is_life","cust_name","con_num","open_ins","open_no","jy_count","jy_num","day_avg","all_jy_count","all_jy_num","is_show","is_ontime","can_use_acc","used_acc","acc_detail","is_quit"]
#     list_filter = [
#         "yearm","open_no"
#     ]
#     list_quick_filter = [{"field": "open_ins", "limit": 10}]
#     # date_hierarchy = 'yearm'
#     # search_fields = ["open_no"]
#     reversion_enable = False
#     list_export = ('xls',)
#     list_export1 = ('xls',)
#     # relfield_style = "fk-select"0.
#
#
#
#     reversion_enable = True
#     import_excel = True
#
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("open_no")
#
#     def get_list_queryset(self):
#         print('self.request', self.request)
#         queryset = super().get_list_queryset()
#         if self.user.is_superuser:
#             return queryset
#         print(self.user,'self.request.user',self.request.user)
#         aa=usergroupinfo.objects.filter(userinfo=self.user).first()
#         groupidlist =[]
#         if aa and aa.group:
#             print('aa',aa,aa.group.all())
#             for a in aa.group.all():
#                 groupidlist.append(a.group_no)
#         queryset = queryset.filter(open_no__in=groupidlist)
#         return queryset
#
#     def post(self, request, *args, **kwargs):
#         #  导入逻辑
#         if 'excel' in request.FILES:
#             print('excel',request.FILES,'month',request.POST.get('month'))
#             opmonth = request.POST.get('month')
#             wb = xlrd.open_workbook(
#                 filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
#             table = wb.sheets()[0]
#             row = table.nrows
#             t1col = ['账号', '开户机构', '客户名', '身份证', '交易笔数', '交易金额']
#             t1col2 = ['机构名称', '挂靠机构号', '法人名称', '法人身份证', '卡号', '日均', '交易总金额', '交易总笔数']
#             t1col3 = ['身份证', '客户名', '百富生活圈折扣', '是否展示易拉宝', '是否按时还款', '是否清退', '本月消费积分', '积分消费详情','缴纳利息','投诉次数']
#             tflag=0
#             add_litreat_list = []
#             op_icc_list=[]
#             #获取账号归属机构列表
#             print(self.user, 'self.request.user', self.request.user)
#
#             groupidlist = []
#             if not self.user.is_superuser:
#                 aa = usergroupinfo.objects.filter(userinfo=self.user).first()
#                 # print('aa', aa, aa.group.all())
#                 for a in aa.group.all():
#                     groupidlist.append(a.group_no)
#             # queryset = queryset.filter(open_no__in=groupidlist)
#             for i in range(0, row):
#                 col = table.row_values(i)
#                 print('col',col)
#                 if i==0 and t1col==col:
#                     print('是表一')
#                     tflag=1
#                 elif i==0 and t1col2==col:
#                     print('是表二')
#                     tflag=2
#                 elif i==0 and t1col3==col:
#                     print('是表三')
#                     tflag=3
#
#                 if i>0:
#                     if tflag==1:
#                         #处理表1数据
#                         op_icc_list.append(col[3])
#                         aa = litreat.objects.filter(yearm=opmonth,icc_id=col[3])
#                         print('aa',aa)
#                         bb = groupinfo.objects.filter(group_no=col[1]).first()
#                         if not bb:
#                             obj = groupinfo(
#                                 group_no=col[1],
#                                 group_name=col[1],
#                             )
#                             obj.save()
#                         #非超级管理员只能导入部分行的数据
#                         if not self.user.is_superuser and col[1] not in groupidlist:
#                             print(col[1],'col[1] not in groupidlist',groupidlist)
#                             continue
#
#
#
#                         if aa:
#                             #有值更新
#                             litreat.objects.filter(yearm=opmonth, icc_id=col[3]).update(
#                                 con_num=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 jy_count=col[4],
#                                 jy_num=col[5],
#                             )
#                         else:
#                             #无值新增
#                             obj = litreat(
#                                 yearm=opmonth,
#                                 icc_id=col[3],
#                                 con_num=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 jy_count=col[4],
#                                 jy_num=col[5],
#                             )
#                             add_litreat_list.append(obj)
#                     if tflag==2:
#                         #处理表1数据
#                         op_icc_list.append(col[3])
#                         aa = litreat.objects.filter(yearm=opmonth,icc_id=col[3])
#                         bb = groupinfo.objects.filter(group_no=col[1]).first()
#                         if not bb:
#                             obj = groupinfo(
#                                 group_no=col[1],
#                                 group_name=col[0],
#                             )
#                             obj.save()
#                         else:
#                             groupinfo.objects.filter(group_no=col[1]).update(
#                                 group_name=col[0],
#                             )
#                         print('aa',aa)
#                         if aa:
#                             #有值更新
#                             litreat.objects.filter(yearm=opmonth, icc_id=col[3]).update(
#                                 open_ins=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 day_avg=col[5],
#                                 all_jy_count=col[7],
#                                 all_jy_num=col[6],
#                             )
#                         else:
#                             #无值新增
#                             obj = litreat(
#                                 yearm=opmonth,
#                                 icc_id=col[3],
#                                 con_num=col[4],
#                                 open_ins=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 day_avg=col[5],
#                                 all_jy_count=col[7],
#                                 all_jy_num=col[6],
#                             )
#                             add_litreat_list.append(obj)
#                             print('add_litreat_list',add_litreat_list)
#                     if tflag==3:
#                         #处理表1数据
#                         op_icc_list.append(col[0])
#                         aa = litreat.objects.filter(yearm=opmonth,icc_id=col[0])
#                         print('aa',aa)
#                         if aa:
#                             #有值更新
#                             litreat.objects.filter(yearm=opmonth, icc_id=col[0]).update(
#                                 is_life=col[2],
#                                 is_show=False if (col[3] == '否') else True,
#                                 is_ontime=False if (col[4] == '否') else True,
#                                 used_acc=col[6],
#                                 acc_detail=col[7],
#                                 jnlx_num=col[8],
#                                 is_quit=False if (col[5] == '否') else True,
#                                 ts_count=col[9],
#                             )
#                         else:
#                             #无值新增
#                             obj = litreat(
#                                 yearm=opmonth,
#                                 icc_id=col[0],
#                                 cust_name=col[1],
#                                 is_life=col[2],
#                                 is_show=False if(col[3]=='否')else True,
#                                 is_ontime=False if(col[4]=='否')else True,
#                                 used_acc=col[6],
#                                 acc_detail=col[7],
#                                 jnlx_num=col[8],
#                                 is_quit=False if(col[5]=='否')else True,
#                                 ts_count=col[9],
#                             )
#                             add_litreat_list.append(obj)
#                             print('add_litreat_list',add_litreat_list)
#             if add_litreat_list != []:
#                 litreat.objects.bulk_create(add_litreat_list)
#             updatejf(opmonth,op_icc_list)
#             pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
#         # return super(litreatAdmin, self).post(request, *args, **kwargs)  # 此返回值必须是这样
#         return super().post(request, *args, **kwargs)

@xadmin.sites.register(usergroupinfo)
class grouAdmin(object):
    list_display = [ "userinfo","group"]
    list_display_links = ("userinfo",)
    # wizard_form_list = [
    #     ("First's Form", ("name", "description")),
    #     ("Second Form", ("contact", "telphone", "address")),
    #     ("Thread Form", ("customer_id",))
    # ]
    # search_fields = [ "yearm","icc_id","nowm_acc","all_acc","is_life","cust_name","con_num","open_ins","open_no","jy_count","jy_num","day_avg","all_jy_count","all_jy_num","is_show","is_ontime","can_use_acc","used_acc","acc_detail","is_quit"]
    # list_filter = [
    #     "yearm","open_no"
    # ]
    # list_quick_filter = [{"field": "open_ins", "limit": 10}]
    # date_hierarchy = 'yearm'
    # search_fields = ["open_no"]
    reversion_enable = False
    # list_export = ('xls',)
    # list_export1 = ('xls',)
    # relfield_style = "fk-select"0.



    # reversion_enable = True
    # import_excel = True

    # actions = [BatchChangeAction, ]
    # batch_fields = ("open_no")

# @xadmin.sites.register(litreatCollect)
# class litreatCollectAdmin(object):
#     list_display = [ "cust_name","icc_id","all_acc","avg_acc","is_life","is_show","all_jy_count","all_jy_num","day_avg","jy_count","jy_num"]
#     list_display_links = ("icc_id",)
#     # wizard_form_list = [
#     #     ("First's Form", ("name", "description")),
#     #     ("Second Form", ("contact", "telphone", "address")),
#     #     ("Thread Form", ("customer_id",))
#     # ]
#     search_fields = [ "icc_id","all_acc","is_life","cust_name",]
#     # list_filter = [
#     #     "yearm","open_no"
#     # ]
#     list_quick_filter = [{"field": "icc_id", "limit": 10}]
#     # date_hierarchy = 'yearm'
#     # search_fields = ["open_no"]
#     reversion_enable = False
#     list_export = ('xls',)
#     list_export1 = ('xls',)
#     # relfield_style = "fk-select"0.
#
#
#
#     reversion_enable = True
#     import_excel = True
#
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("open_no")
#
#     def get_list_queryset(self):
#         print('self.request', self.request)
#         queryset = super().get_list_queryset()
#         if self.user.is_superuser:
#             return queryset
#         print(self.user,'self.request.user',self.request.user)
#         aa=usergroupinfo.objects.filter(userinfo=self.user).first()
#         groupidlist =[]
#         if aa and aa.group:
#             print('aa',aa,aa.group.all())
#             for a in aa.group.all():
#                 groupidlist.append(a.group_no)
#         queryset = queryset.filter(open_no__in=groupidlist)
#         return queryset
#
#     def post(self, request, *args, **kwargs):
#         #  导入逻辑
#         if 'excel' in request.FILES:
#             print('excel',request.FILES,'month',request.POST.get('month'))
#             opmonth = request.POST.get('month')
#             wb = xlrd.open_workbook(
#                 filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
#             table = wb.sheets()[0]
#             row = table.nrows
#             t1col = ['账号', '开户机构', '客户名', '身份证', '交易笔数', '交易金额']
#             t1col2 = ['机构名称', '挂靠机构号', '法人名称', '法人身份证', '卡号', '日均', '交易总金额', '交易总笔数']
#             t1col3 = ['身份证', '客户名', '百富生活圈折扣', '是否展示易拉宝', '是否按时还款', '是否清退', '本月消费积分', '积分消费详情','缴纳利息','投诉次数']
#             tflag=0
#             add_litreat_list = []
#             op_icc_list=[]
#             #获取账号归属机构列表
#             print(self.user, 'self.request.user', self.request.user)
#
#             groupidlist = []
#             if not self.user.is_superuser:
#                 aa = usergroupinfo.objects.filter(userinfo=self.user).first()
#                 # print('aa', aa, aa.group.all())
#                 for a in aa.group.all():
#                     groupidlist.append(a.group_no)
#             # queryset = queryset.filter(open_no__in=groupidlist)
#             for i in range(0, row):
#                 col = table.row_values(i)
#                 print('col',col)
#                 if i==0 and t1col==col:
#                     print('是表一')
#                     tflag=1
#                 elif i==0 and t1col2==col:
#                     print('是表二')
#                     tflag=2
#                 elif i==0 and t1col3==col:
#                     print('是表三')
#                     tflag=3
#
#                 if i>0:
#                     if tflag==1:
#                         #处理表1数据
#                         op_icc_list.append(col[3])
#                         aa = litreat.objects.filter(yearm=opmonth,icc_id=col[3])
#                         print('aa',aa)
#                         bb = groupinfo.objects.filter(group_no=col[1]).first()
#                         if not bb:
#                             obj = groupinfo(
#                                 group_no=col[1],
#                                 group_name=col[1],
#                             )
#                             obj.save()
#                         #非超级管理员只能导入部分行的数据
#                         if not self.user.is_superuser and col[1] not in groupidlist:
#                             print(col[1],'col[1] not in groupidlist',groupidlist)
#                             continue
#
#
#
#                         if aa:
#                             #有值更新
#                             litreat.objects.filter(yearm=opmonth, icc_id=col[3]).update(
#                                 con_num=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 jy_count=col[4],
#                                 jy_num=col[5],
#                             )
#                         else:
#                             #无值新增
#                             obj = litreat(
#                                 yearm=opmonth,
#                                 icc_id=col[3],
#                                 con_num=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 jy_count=col[4],
#                                 jy_num=col[5],
#                             )
#                             add_litreat_list.append(obj)
#                     if tflag==2:
#                         #处理表1数据
#                         op_icc_list.append(col[3])
#                         aa = litreat.objects.filter(yearm=opmonth,icc_id=col[3])
#                         bb = groupinfo.objects.filter(group_no=col[1]).first()
#                         if not bb:
#                             obj = groupinfo(
#                                 group_no=col[1],
#                                 group_name=col[0],
#                             )
#                             obj.save()
#                         else:
#                             groupinfo.objects.filter(group_no=col[1]).update(
#                                 group_name=col[0],
#                             )
#                         print('aa',aa)
#                         if aa:
#                             #有值更新
#                             litreat.objects.filter(yearm=opmonth, icc_id=col[3]).update(
#                                 open_ins=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 day_avg=col[5],
#                                 all_jy_count=col[7],
#                                 all_jy_num=col[6],
#                             )
#                         else:
#                             #无值新增
#                             obj = litreat(
#                                 yearm=opmonth,
#                                 icc_id=col[3],
#                                 con_num=col[4],
#                                 open_ins=col[0],
#                                 open_no=col[1],
#                                 cust_name=col[2],
#                                 day_avg=col[5],
#                                 all_jy_count=col[7],
#                                 all_jy_num=col[6],
#                             )
#                             add_litreat_list.append(obj)
#                             print('add_litreat_list',add_litreat_list)
#                     if tflag==3:
#                         #处理表1数据
#                         op_icc_list.append(col[0])
#                         aa = litreat.objects.filter(yearm=opmonth,icc_id=col[0])
#                         print('aa',aa)
#                         if aa:
#                             #有值更新
#                             litreat.objects.filter(yearm=opmonth, icc_id=col[0]).update(
#                                 is_life=col[2],
#                                 is_show=False if (col[3] == '否') else True,
#                                 is_ontime=False if (col[4] == '否') else True,
#                                 used_acc=col[6],
#                                 acc_detail=col[7],
#                                 jnlx_num=col[8],
#                                 is_quit=False if (col[5] == '否') else True,
#                                 ts_count=col[9],
#                             )
#                         else:
#                             #无值新增
#                             obj = litreat(
#                                 yearm=opmonth,
#                                 icc_id=col[0],
#                                 cust_name=col[1],
#                                 is_life=col[2],
#                                 is_show=False if(col[3]=='否')else True,
#                                 is_ontime=False if(col[4]=='否')else True,
#                                 used_acc=col[6],
#                                 acc_detail=col[7],
#                                 jnlx_num=col[8],
#                                 is_quit=False if(col[5]=='否')else True,
#                                 ts_count=col[9],
#                             )
#                             add_litreat_list.append(obj)
#                             print('add_litreat_list',add_litreat_list)
#             if add_litreat_list != []:
#                 litreat.objects.bulk_create(add_litreat_list)
#             updatejf(opmonth,op_icc_list)
#             pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
#         # return super(litreatAdmin, self).post(request, *args, **kwargs)  # 此返回值必须是这样
#         return super().post(request, *args, **kwargs)



def updatejf(yearmonth,icc_list):
    print('更新月份积分yearmonth',yearmonth)
    tmp_list = icc_list
    for col in icc_list:
        aa = litreat.objects.filter(yearm=yearmonth, icc_id=col)
        print('aaaaa',len(aa))
        if len(aa)==0:
            continue
        aa = litreat.objects.filter(yearm=yearmonth,icc_id=col)[0]#.first()
        #计算本条积分，更新表字段
        # 生活圈按折扣对应积分
        zkjf={'10.00-9.60':0,'9.60-9.20':100,'9.20-8.80':120,'8.80-8.00':130,'8.00-7.00':150,'7.00-6.50':180,'6.50-0.00':200,}
        lifezk = '10.00-9.60'
        nowjf = 0
        print('aa1212',aa,aa.is_life)
        if aa.is_life:

            for key in zkjf:
                print(key + ':' + str(zkjf[key]))
                bb = key.split('-')
                print(float(bb[1]),float(aa.is_life),float(bb[0]),(float(aa.is_life)>float(bb[1]) and float(aa.is_life)<=float(bb[0])))
                if float(aa.is_life)>float(bb[1]) and float(aa.is_life)<=float(bb[0]):
                    lifezk = key
                    break
            print(aa.is_life,'aaa',lifezk)

            #本月积分  是否生活圈*100+Limit(交易总笔数*1,200)+Limit(int(总交易金额/100)*1,300)+Limit(int(日均/1000)*1,200)+Limit(交易笔数*1,10)+Limit(int(交易金额/100)*1,10)
            print('zkjf[lifezk]',zkjf[lifezk])
            nowjf = zkjf[lifezk]+(aa.all_jy_count*1 if(aa.all_jy_count*1<200)else 200)+(int(aa.all_jy_num/100) if(int(aa.all_jy_num/100)<300)else 300) \
                    + (int(aa.day_avg/1000) if(int(aa.day_avg/1000)<200)else 200) \
                    + (int(aa.jy_count/1) if(int(aa.jy_count/1)<10)else 10) \
                    + (int(aa.jy_num/100) if(int(aa.jy_num/100)<10)else 10) \
                    + (int(aa.jnlx_num/500) if(int(aa.jnlx_num/500)<200)else 200) \
                    + aa.is_show*100
            print(aa.icc_id,'nowjf',nowjf)
        else:
            nowjf = (aa.all_jy_count * 1 if (aa.all_jy_count * 1 < 200) else 200) + (
                int(aa.all_jy_num / 100) if (int(aa.all_jy_num / 100) < 300) else 300) \
                    + (int(aa.day_avg / 1000) if (int(aa.day_avg / 1000) < 200) else 200) \
                    + (int(aa.jy_count / 1) if (int(aa.jy_count / 1) < 10) else 10) \
                    + (int(aa.jy_num / 100) if (int(aa.jy_num / 100) < 10) else 10) \
                    + (int(aa.jnlx_num / 500) if (int(aa.jnlx_num / 500) < 200) else 200) \
                    + aa.is_show * 100
            print(aa.icc_id, 'nowjf', nowjf)

        alljf = nowjf
        #总积分=year.months-1.id.总积分+本月积分-（year.months-1.id.是否展示易拉宝）*100-（year.months-1.id.是否生活圈）*100

        startTime = datetime.datetime.strptime(yearmonth, '%Y-%m')
        # 前一个月最后一天
        pre_month = startTime.replace(day=1) - datetime.timedelta(days=1)  # timedelta是一个不错的函数
        pre_month_str = datetime.datetime.strftime(pre_month, "%Y-%m")
        print('pre_month_str',pre_month_str)
        bb = litreat.objects.filter(yearm=pre_month_str, icc_id=col).first()
        if bb:
            alljf = bb.all_acc + nowjf - bb.is_show*100-zkjf[lifezk]
            if alljf<0:
                alljf=0
        kyjf = nowjf -aa.used_acc
        #可用积分=year.months-1.id.可用积分+本月积分-（year.months-1.id.是否展示易拉宝）*100-（year.months-1.id.是否生活圈）*100-积分消费记录
        if bb:
            kyjf = bb.can_use_acc + nowjf -zkjf[lifezk] -aa.used_acc - bb.is_show*100

        litreat.objects.filter(yearm=yearmonth, icc_id=col).update(
            nowm_acc=nowjf,
            all_acc=alljf,
            can_use_acc=kyjf,
        )
        # 更新月均积分值 avg_acc
        startTime1 = datetime.datetime.strptime(yearmonth, '%Y-%m')
        # 前一个月最后一天
        pre_month1 = startTime1.replace(day=1) - datetime.timedelta(days=1)  # timedelta是一个不错的函数
        # startTime1 = datetime.datetime.strptime(pre_month1, '%Y-%m')
        for i in range(1, 11):
            pre_month1 = pre_month1.replace(day=1) - datetime.timedelta(days=1)  # timedelta是一个不错的函数
            # startTime1 = datetime.datetime.strptime(pre_month1, '%Y-%m')
        endym = datetime.datetime.strftime(pre_month1, "%Y-%m")
        print('1111yearmonth', yearmonth, 'pre_month1', pre_month1, 'endym', endym)
        avgjf = litreat.objects.filter(yearm__lte=yearmonth, yearm__gte=endym, icc_id=col).aggregate(Avg('nowm_acc'))

        print('1111yearmonth', yearmonth, 'pre_month1', pre_month1, 'avgjf', avgjf)
        litreat.objects.filter(yearm=yearmonth, icc_id=col).update(
            avg_acc=avgjf['nowm_acc__avg'],
        )
    #获取当前月及12月前时间，判断yearmonth+1个月是否小于当前年月且在当前年月前12个月内，则操作
    startTime = datetime.datetime.strptime(yearmonth, '%Y-%m')
    # 前一个月最后一天
    pre_month = startTime.replace(day=1) - datetime.timedelta(days=1)  # timedelta是一个不错的函数
    pre_month_str = datetime.datetime.strftime(pre_month, "%Y-%m")
    # 求后一个月的第一天
    days_num = calendar.monthrange(startTime.year, startTime.month)[1]  # 获取一个月有多少天
    first_day_of_next_month = startTime + datetime.timedelta(days=days_num)  # 当月的最后一天只需要days_num-1即可
    next_month_str = datetime.datetime.strftime(first_day_of_next_month, "%Y-%m")
    print(u'后一个月的第一天:' + str(first_day_of_next_month))
    if first_day_of_next_month<datetime.datetime.now():
        updatejf(next_month_str, tmp_list)




#
# @xadmin.sites.register(kmChoices)
# class kmChoicesAdmin(object):
#     list_display = ("description",)
#     list_display_links = ("description",)
#     wizard_form_list = [
#         ("First's Form", ("name", "description")),
#         ("Second Form", ("contact", "telphone", "address")),
#         ("Thread Form", ("customer_id",))
#     ]
#     search_fields = [ "description"]
#     list_filter = [
#         "description"
#     ]
#     list_quick_filter = [{"field": "description", "limit": 10}]
#
#     search_fields = ["description"]
#     relfield_style = "fk-select"
#     reversion_enable = True
#
#     actions = [BatchChangeAction, ]
#     batch_fields = ("description")

# @xadmin.sites.register(IDC)
# class IDCAdmin(object):
#     list_display = ("name", "description", "create_time", "contact", "telphone", "address", "customer_id")
#     list_display_links = ("name",)
#     wizard_form_list = [
#         ("First's Form", ("name", "description")),
#         ("Second Form", ("contact", "telphone", "address")),
#         ("Thread Form", ("customer_id",))
#     ]
#     search_fields = ["name", "description", "contact", "telphone", "address"]
#     list_filter = [
#         "name"
#     ]
#     list_quick_filter = [{"field": "name", "limit": 10}]
#
#     search_fields = ["name"]
#     relfield_style = "fk-select"
#     reversion_enable = True
#
#     actions = [BatchChangeAction, ]
#     batch_fields = ("contact", "description", "address", "customer_id")

#
# @xadmin.sites.register(Host)
# class HostAdmin(object):
#
#     def open_web(self, instance):
#         return """<a href="http://%s" target="_blank">Open</a>""" % instance.ip
#
#     open_web.short_description = "Acts"
#     open_web.allow_tags = True
#     open_web.is_column = True
#
#     list_display = (
#         "name", "idc", "guarantee_date", "service_type", "status", "open_web",
#         "description", "ip",
#     )
#     list_display_links = ("name",)
#
#     raw_id_fields = ("idc",)
#     style_fields = {"system": "radio-inline"}
#
#     search_fields = ["name", "ip", "description", "idc__name"]
#     list_filter = [
#         "idc", "guarantee_date", "status", "brand", "model", "cpu", "core_num",
#         "hard_disk", "memory", (
#             "service_type",
#             xadmin.filters.MultiSelectFieldListFilter,
#         ),
#     ]
#
#     list_quick_filter = ["service_type", {"field": "idc__name", "limit": 10}]
#     # list_quick_filter = ["idc_id"]
#     list_bookmarks = [{
#         "title": "Need Guarantee",
#         "query": {"status__exact": 2},
#         "order": ("-guarantee_date",),
#         "cols": ("brand", "guarantee_date", "service_type"),
#     }]
#
#     show_detail_fields = ("idc",)
#     list_editable = (
#         "name", "idc", "guarantee_date", "service_type", "description", "ip"
#     )
#     save_as = True
#
#     aggregate_fields = {"guarantee_date": "min"}
#     grid_layouts = ("table", "thumbnails")
#
#     form_layout = (
#         Main(
#             TabHolder(
#                 Tab(
#                     "Comm Fields",
#                     Fieldset(
#                         "Company data", "name", "idc",
#                         description="some comm fields, required",
#                     ),
#                     Inline(MaintainLog),
#                 ),
#                 Tab(
#                     "Extend Fields",
#                     Fieldset(
#                         "Contact details",
#                         "service_type",
#                         Row("brand", "model"),
#                         Row("cpu", "core_num"),
#                         Row(
#                             AppendedText("hard_disk", "G"),
#                             AppendedText("memory", "G")
#                         ),
#                         "guarantee_date"
#                     ),
#                 ),
#             ),
#         ),
#         Side(
#             Fieldset("Status data", "status", "ssh_port", "ip"),
#         )
#     )
#     inlines = [MaintainInline]
#     reversion_enable = True
#
#     data_charts = {
#         "host_service_type_counts": {'title': u"Host service type count", "x-field": "service_type",
#                                      "y-field": ("service_type",),
#                                      "option": {
#                                          "series": {"bars": {"align": "center", "barWidth": 0.8, 'show': True}},
#                                          "xaxis": {"aggregate": "count", "mode": "categories"},
#                                      },
#                                      },
#     }





# @xadmin.sites.register(ccpa)
# class ccpaAdmin(object):
#     list_display = (
#         "name", "phone", "edu", "periods", "train", "area")
#     list_display_links = ("name",)
#
#     list_filter = ["edu", "periods", "train", "area"]
#     search_fields = ["name"]
#
#     form_layout = (
#         Col("col2",
#             Fieldset("Record data",
#                      "time", "note",
#                      css_class="unsort short_label no_title"
#                      ),
#             span=9, horizontal=True
#             ),
#         Col("col1",
#             Fieldset("Comm data",
#                      "host", "maintain_type"
#                      ),
#             Fieldset("Maintain details",
#                      "hard_type", "operator"
#                      ),
#             span=3
#             )
#     )
#     reversion_enable = True

# @xadmin.sites.register(ccpa)
# class ccpaAdmin(object):
#     list_display = ('card_no',"name", "phone", "edu", "periods", "train", "area",'status')
#     list_editable = [ 'status']
#     list_printable = ['status']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     search_fields = ["name", "phone", "train", "area"]
#     list_filter = [
#         "name"
#     ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     exclude = ['status','train']
#     # free_query_filter = True
#     # search_fields = ["train","name"]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     actions = [BatchChangeAction, ]
#     batch_fields = ("name", "phone", "edu", "periods")
#
#
#     def get_list_queryset(self):
#         print('self.request', self.request)
#         queryset = super().get_list_queryset()
#         if self.user.is_superuser:
#             return queryset
#         queryset = queryset.filter(train=self.request.user)
#         return queryset
#     def save_models(self):
#         # print('121212self.request', self.request,self)
#         flag = self.org_obj is None and 'create' or 'change'
#         if flag=='create':
#             self.new_obj.train_id = str(self.request.user.id)
#         super().save_models()

# @xadmin.sites.register(xss)
# class xssAdmin(object):
#     list_display = ("card_no","name","phone", "edu", "periods", "train", "area","status")
#     list_printable = [ 'status']
#     list_editable = ['status']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     search_fields = ["name", "phone"]
#     list_filter = [
#         "name"
#     ]
#     exclude = ['status','train']
#     # inlines = ['status']
#
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # free_query_filter = True
#     # search_fields = ["train","name"]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     actions = [BatchChangeAction, ]
#     batch_fields = ("name", "phone", "edu", "periods")
#
#     # def status_view(self, obj):
#     #     return obj.status
#
#     def get_list_queryset(self):
#         print('self.request', self.request)
#         queryset = super().get_list_queryset()
#         print('self.queryset', self.queryset)
#         if self.user.is_superuser:
#             return queryset
#         queryset = queryset.filter(train=self.request.user)
#         return queryset
#
#     def save_models(self):
#         # print('121212self.request', self.request,self)
#         flag = self.org_obj is None and 'create' or 'change'
#         if flag=='create':
#             self.new_obj.train_id = str(self.request.user.id)
#         super().save_models()
#
#     # def get_form_datas(self):
#     #     print('self.request', self.request)
#     #     queryset = super().get_form_datas()
#     #     print('queryset', queryset)
#     #     return queryset
#
#     # def get_context(self):
#     #     new_context = {
#     #         'card_no': ('Add %s') % '12',
#     #     }
#     #     context = super().get_context()
#     #     context.update(new_context)
#     #     print('context',context)
#     #     return context
#
#     # def result_item(self):
#     #     print('result_item0')
#     #     return super().result_item()
#         # queryset = super().result_item(self)
#         # print('queryset')
#         # return queryset
#
#
#     # def get_form_datas(self):
#     #     queryset = super().get_form_datas()
#     #     print('get_form_datas', queryset) #,queryset['instance'].status 新数据无instance
#     #     return queryset
#         # data = {'initial': self.get_initial_data()}
#         # if self.request_method == 'get':
#         #     data['initial'].update(self.request.GET)
#         # else:
#         #     data.update({'data': self.request.POST, 'files': self.request.FILES})
#         # return data
#
#     # def queryset(self):
#     #
#     #     """函数作用：使当前登录的用户只能看到自己负责的服务器"""
#     #     # qs = super(ccpaAdmin, self).queryset(self)
#     #     return super(ccpaAdmin, self).queryset(self)
#         # if request.user.is_superuser:
#         #     return qs
#         # return qs.filter(user=ccpa.objects.filter(train_name=request.user))

# @xadmin.sites.register(treatment)
# class treatmentAdmin(object):
#     list_display = ('cust',"date", "item","prov","minute", "hicaps", "cash", "cost")
#     # list_editable = [ 'status']
#     list_printable = ['cust']
#     list_Print = ('cust')
#     date_hierarchy = 'date'
#     # data_charts = {
#     #     "user_count": {'title': u"Treatment Report", "x-field": "date", "y-field": ("prov_count",),
#     #                    "order": ('date',)},
#     #     # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
#     # }
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     # search_fields = ['cust',"date", "item"]
#     list_filter = [
#         'cust',"date", "item"
#     ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # exclude = ['status','train']
#     free_query_filter = True
#     search_fields = ['cust__contact_number','cust__first_name','cust__last_name',"date", ]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("name", "phone", "edu", "periods")
#
#
#     def get_list_queryset(self):
#         print('self.request', self.request,self.request.GET.keys())
#         for i in self.request.GET.keys():
#             print(i,self.request.GET.get(i))
#             # self.request.GET[i]='121212'
#
#
#         # for i in self.request.GET.keys():
#         #     print(i,self.request.GET.get(i))
#
#         queryset = super().get_list_queryset()
#         # if self.user.is_superuser:
#         #     return queryset
#         # queryset = queryset.filter(train=self.request.user)
#         return queryset
#     # def save_models(self):
#     #     # print('121212self.request', self.request,self)
#     #     flag = self.org_obj is None and 'create' or 'change'
#     #     if flag=='create':
#     #         self.new_obj.train_id = str(self.request.user.id)
#     #     super().save_models()


# @xadmin.sites.register(customer)
# class customerAdmin(object):
#     list_display = ('fullname',"date_of_birth","contact_number", "health_fund", "health_fund_number")
#     # list_editable = [ 'status'] 'first_name','last_name',
#     # list_printable = ['fullname']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     search_fields = ['first_name',"last_name", "health_fund", "health_fund_number"]
#     list_filter = [
#         'first_name',"last_name", "health_fund", "health_fund_number"
#     ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # exclude = ['status','train']
#     # free_query_filter = True
#     search_fields = ["contact_number",'first_name',"last_name", "health_fund_number"]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("name", "phone", "edu", "periods")
#
#
#
# @xadmin.sites.register(provider)
# class providerAdmin(object):
#     list_display = ('fullname', "health_fund", "health_fund_number")
#     # list_editable = [ 'status']
#     # list_printable = ['health_fund_number']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     search_fields = ['first_name',"last_name", "health_fund", "health_fund_number"]
#     list_filter = [
#         'first_name',"last_name", "health_fund", "health_fund_number"
#     ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # exclude = ['status','train']
#     # free_query_filter = True
#     # search_fields = ["train","name"]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("name", "phone", "edu", "periods")
#
#
# @xadmin.sites.register(fund)
# class fundAdmin(object):
#     list_display = ("name",)
#     # list_editable = ['status']
#     # list_printable = ['status']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     search_fields = ["name",]
#     list_filter = [
#         "name",
#     ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # exclude = ['status', 'train']
#     # free_query_filter = True
#     # search_fields = ["train","name"]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     actions = [BatchChangeAction, ]
#     batch_fields = ("name")
#
#     # list_display = ('name')
#     # list_editable = [ 'status']
#     # list_printable = ['status']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     # search_fields = ['name']
#     # list_filter = [
#     #     'name'
#     # ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # exclude = ['status','train']
#     # free_query_filter = True
#     # search_fields = ["train","name"]
#     # relfield_style = "train"
#     # reversion_enable = False
#     # list_export = ('xls',)
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("name", "phone", "edu", "periods")
#
# @xadmin.sites.register(treatment_item)
# class treatment_itemAdmin(object):
#     list_display = ('name',)
#     # list_editable = [ 'status']
#     # list_printable = ['status']
#     # list_display_links = ("name",)
#     # wizard_form_list = [
#     #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
#     #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
#     #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
#     # ]
#     search_fields = ['name',]
#     list_filter = [
#         'name',
#     ]
#     # list_quick_filter = [{"field": "train", "limit": 10}]
#     # exclude = ['status','train']
#     free_query_filter = True
#     # search_fields = ["train","name"]
#     # relfield_style = "train"
#     reversion_enable = False
#     list_export = ('xls',)
#     # actions = [BatchChangeAction, ]
#     # batch_fields = ("name", "phone", "edu", "periods")




# xadmin.sites.site.register(HostGroup, HostGroupAdmin)
# xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
# xadmin.sites.site.register(IDC, IDCAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
