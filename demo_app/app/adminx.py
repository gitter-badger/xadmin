from __future__ import absolute_import
import xadmin
from xadmin import views
from .models import IDC, Host, MaintainLog, HostGroup, AccessRecord,ccpa,xss,kmChoices,treatment,provider,customer,treatment_item,fund
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

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


# @xadmin.sites.register(views.CommAdminView)
# class GlobalSetting(object):
#     global_search_models = [Host, IDC]
#     global_models_icon = {
#         Host: "fa fa-laptop", IDC: "fa fa-cloud"
#     }
#     menu_style = 'default'  # 'accordion'


class MaintainInline(object):
    model = MaintainLog
    extra = 1
    style = "accordion"

#
@xadmin.sites.register(kmChoices)
class kmChoicesAdmin(object):
    list_display = ("description",)
    list_display_links = ("description",)
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

@xadmin.sites.register(ccpa)
class ccpaAdmin(object):
    list_display = ('card_no',"name", "phone", "edu", "periods", "train", "area",'status')
    list_editable = [ 'status']
    list_printable = ['status']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    search_fields = ["name", "phone", "train", "area"]
    list_filter = [
        "name"
    ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    exclude = ['status','train']
    # free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    actions = [BatchChangeAction, ]
    batch_fields = ("name", "phone", "edu", "periods")


    def get_list_queryset(self):
        print('self.request', self.request)
        queryset = super().get_list_queryset()
        if self.user.is_superuser:
            return queryset
        queryset = queryset.filter(train=self.request.user)
        return queryset
    def save_models(self):
        # print('121212self.request', self.request,self)
        flag = self.org_obj is None and 'create' or 'change'
        if flag=='create':
            self.new_obj.train_id = str(self.request.user.id)
        super().save_models()

@xadmin.sites.register(xss)
class xssAdmin(object):
    list_display = ("card_no","name","phone", "edu", "periods", "train", "area","status")
    list_printable = [ 'status']
    list_editable = ['status']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    search_fields = ["name", "phone"]
    list_filter = [
        "name"
    ]
    exclude = ['status','train']
    # inlines = ['status']

    # list_quick_filter = [{"field": "train", "limit": 10}]
    # free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    actions = [BatchChangeAction, ]
    batch_fields = ("name", "phone", "edu", "periods")

    # def status_view(self, obj):
    #     return obj.status

    def get_list_queryset(self):
        print('self.request', self.request)
        queryset = super().get_list_queryset()
        print('self.queryset', self.queryset)
        if self.user.is_superuser:
            return queryset
        queryset = queryset.filter(train=self.request.user)
        return queryset

    def save_models(self):
        # print('121212self.request', self.request,self)
        flag = self.org_obj is None and 'create' or 'change'
        if flag=='create':
            self.new_obj.train_id = str(self.request.user.id)
        super().save_models()

    # def get_form_datas(self):
    #     print('self.request', self.request)
    #     queryset = super().get_form_datas()
    #     print('queryset', queryset)
    #     return queryset

    # def get_context(self):
    #     new_context = {
    #         'card_no': ('Add %s') % '12',
    #     }
    #     context = super().get_context()
    #     context.update(new_context)
    #     print('context',context)
    #     return context

    # def result_item(self):
    #     print('result_item0')
    #     return super().result_item()
        # queryset = super().result_item(self)
        # print('queryset')
        # return queryset


    # def get_form_datas(self):
    #     queryset = super().get_form_datas()
    #     print('get_form_datas', queryset) #,queryset['instance'].status 新数据无instance
    #     return queryset
        # data = {'initial': self.get_initial_data()}
        # if self.request_method == 'get':
        #     data['initial'].update(self.request.GET)
        # else:
        #     data.update({'data': self.request.POST, 'files': self.request.FILES})
        # return data

    # def queryset(self):
    #
    #     """函数作用：使当前登录的用户只能看到自己负责的服务器"""
    #     # qs = super(ccpaAdmin, self).queryset(self)
    #     return super(ccpaAdmin, self).queryset(self)
        # if request.user.is_superuser:
        #     return qs
        # return qs.filter(user=ccpa.objects.filter(train_name=request.user))

@xadmin.sites.register(treatment)
class treatmentAdmin(object):
    list_display = ('cust',"date", "item","prov","minute", "hicaps", "cash", "cost")
    # list_editable = [ 'status']
    list_printable = ['cust']
    date_hierarchy = 'date'
    # data_charts = {
    #     "user_count": {'title': u"Treatment Report", "x-field": "date", "y-field": ("prov_count",),
    #                    "order": ('date',)},
    #     # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    # }
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    # search_fields = ['cust',"date", "item"]
    list_filter = [
        'cust',"date", "item"
    ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    # exclude = ['status','train']
    free_query_filter = True
    search_fields = ["date", ]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    # actions = [BatchChangeAction, ]
    # batch_fields = ("name", "phone", "edu", "periods")


    # def get_list_queryset(self):
    #     print('self.request', self.request)
    #     queryset = super().get_list_queryset()
    #     if self.user.is_superuser:
    #         return queryset
    #     queryset = queryset.filter(train=self.request.user)
    #     return queryset
    # def save_models(self):
    #     # print('121212self.request', self.request,self)
    #     flag = self.org_obj is None and 'create' or 'change'
    #     if flag=='create':
    #         self.new_obj.train_id = str(self.request.user.id)
    #     super().save_models()


@xadmin.sites.register(customer)
class customerAdmin(object):
    list_display = ('fullname',"date_of_birth","contact_number", "health_fund", "health_fund_number")
    # list_editable = [ 'status'] 'first_name','last_name',
    # list_printable = ['fullname']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    search_fields = ['first_name',"last_name", "health_fund", "health_fund_number"]
    list_filter = [
        'first_name',"last_name", "health_fund", "health_fund_number"
    ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    # exclude = ['status','train']
    # free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    # actions = [BatchChangeAction, ]
    # batch_fields = ("name", "phone", "edu", "periods")



@xadmin.sites.register(provider)
class providerAdmin(object):
    list_display = ('fullname', "health_fund", "health_fund_number")
    # list_editable = [ 'status']
    list_printable = ['health_fund_number']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    search_fields = ['first_name',"last_name", "health_fund", "health_fund_number"]
    list_filter = [
        'first_name',"last_name", "health_fund", "health_fund_number"
    ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    # exclude = ['status','train']
    # free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    # actions = [BatchChangeAction, ]
    # batch_fields = ("name", "phone", "edu", "periods")


@xadmin.sites.register(fund)
class fundAdmin(object):
    list_display = ("name",)
    # list_editable = ['status']
    # list_printable = ['status']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    search_fields = ["name",]
    list_filter = [
        "name",
    ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    # exclude = ['status', 'train']
    # free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    actions = [BatchChangeAction, ]
    batch_fields = ("name")

    # list_display = ('name')
    # list_editable = [ 'status']
    # list_printable = ['status']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    # search_fields = ['name']
    # list_filter = [
    #     'name'
    # ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    # exclude = ['status','train']
    # free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    # reversion_enable = False
    # list_export = ('xls',)
    # actions = [BatchChangeAction, ]
    # batch_fields = ("name", "phone", "edu", "periods")

@xadmin.sites.register(treatment_item)
class treatment_itemAdmin(object):
    list_display = ('name',)
    # list_editable = [ 'status']
    # list_printable = ['status']
    # list_display_links = ("name",)
    # wizard_form_list = [
    #     ("第一步", ( "area", "train", "periods","name","pinyin","sex", "guarantee_date", "nation","edu", "poilt", "icc","phone","email")),
    #     ("第二步", ("school", "work", "job","address","enaddress","Postcodes","telephone")),
    #     ("第三步", ("type","kskm","exam_date","exam_address","photo"))
    # ]
    search_fields = ['name',]
    list_filter = [
        'name',
    ]
    # list_quick_filter = [{"field": "train", "limit": 10}]
    # exclude = ['status','train']
    free_query_filter = True
    # search_fields = ["train","name"]
    # relfield_style = "train"
    reversion_enable = False
    list_export = ('xls',)
    # actions = [BatchChangeAction, ]
    # batch_fields = ("name", "phone", "edu", "periods")




# xadmin.sites.site.register(HostGroup, HostGroupAdmin)
# xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
# xadmin.sites.site.register(IDC, IDCAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
