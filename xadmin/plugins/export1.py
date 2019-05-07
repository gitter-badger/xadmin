import io
import datetime
import sys

from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from future.utils import iteritems

from django.http import HttpResponse
from django.template import loader
from django.utils import six
from django.utils.encoding import force_text, smart_text
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.xmlutils import SimplerXMLGenerator
from django.db.models import BooleanField, NullBooleanField

from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.util import json
from xadmin.views.list import ALL_VAR

try:
    import xlwt
    has_xlwt = True
except:
    has_xlwt = False

try:
    import xlsxwriter
    has_xlsxwriter = True
except:
    has_xlsxwriter = False


class ExportMenuPlugin1(BaseAdminPlugin):

    list_export1 = ( 'xls',)
    export_names1 = { 'xls': 'Excel'}

    def init_request(self, *args, **kwargs):
        print('ExportMenuPlugin11111')
        self.request.GET.get('_do_') == 'export'
        self.list_export1 = [
            f for f in self.list_export1
            if (f != 'xlsx' or has_xlsxwriter) and (f != 'xls' or has_xlwt)]

    def block_top_toolbar(self, context, nodes):
        if self.list_export1:
            context.update({
                'show_export_all': self.admin_view.paginator.count > self.admin_view.list_per_page and not ALL_VAR in self.admin_view.request.GET,
                'form_params': self.admin_view.get_form_params({'print': 'true'}, ('export_type',)),
                'export_types': [{'type': et, 'name': self.export_names1[et]} for et in self.list_export1],
            })
            nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.exports1.html',
                                                 context=get_context_dict(context)))
    def formdata(self,datas):
        print('datas',datas)
        datetime_now = datetime.datetime.now()
        datetime_three_month_ago = datetime_now - relativedelta(months=3)
        untilMonth = datetime_three_month_ago.strftime('%Y-%m')
        print(datetime_now,'datetime_three_month_ago',datetime_three_month_ago,untilMonth)
        #年月 身份证 名字 账号 开户行 本月积分
        limitlist=['记录年月', '身份证号', '客户名', '账号', '开户机构', '本月积分',]

        limitidlist=[]
        returndata=[]
        i=0
        headlist=[]
        msg = {'code':'ok','msg':'正确'}
        months=0
        lilv=0
        jfsum=0
        name=''
        maxmonth=4
        for d1 in datas:
            i=i+1

            if i==1:
                j=0
                for d0 in d1:
                    if d0 in limitlist:
                        headlist.append(d0)
                        limitidlist.append(j)
                    j=j+1
                print('headlist',headlist)
                returndata.append(headlist)
            else:
                datalist=[]
                if d1[1] >= untilMonth:
                    months = months + 1
                    print('计算了', i, '个月')
                # else:

                for j in limitidlist:
                    j=j+1
                    datalist.append(d1[j-1])
                    if j==2:
                        #姓名

                        if name !='' and name!=d1[3]:
                            print('name q11111',name,j,d1)
                            msg['code']='err'
                            msg['msg']='不止一个人'
                        name=d1[3]
                    if j>8:
                        #本月积分  每行取当月积分累加

                        if d1[1] >= untilMonth:
                            print('计算了', i, '个月')
                            jfsum = jfsum + int(d1[5])
                        else:
                            print(d1, 'abcd', j)


                print('datalist',datalist)
                returndata.append(datalist)
        pjjf = jfsum/months
        print(' pjjf = jfsum/months', pjjf,jfsum,months)
        if pjjf>=600 and pjjf<650:
            lilv=5
        elif  pjjf>=650 and pjjf<700:
            lilv=10
        elif  pjjf>=700 and pjjf<750:
            lilv=15
        elif  pjjf>=750 and pjjf<800:
            lilv=20
        elif  pjjf>=800 and pjjf<850:
            lilv=25
        elif  pjjf>=850 and pjjf<900:
            lilv=30
        elif  pjjf>=900 and pjjf<950:
            lilv=35
        elif  pjjf>=950:
            lilv=40
        replacedata = {'_name_': name, '_month_':months, '_lilv_': str(lilv)+'%'}
        print('replacedata',replacedata)
        return returndata,replacedata,msg
    def _format_value(self, o):
        if (o.field is None and getattr(o.attr, 'boolean', False)) or \
           (o.field and isinstance(o.field, (BooleanField, NullBooleanField))):
                value = o.value
        elif str(o.text).startswith("<span class='text-muted'>"):
            value = escape(str(o.text)[25:-7])
        else:
            value = escape(str(o.text))
        return value
    def _get_datas(self, context):
        rows = context['results']
        print('rows',type(rows),rows)
        #
        new_rows = [[self._format_value(o) for o in
                     r.cells] for r in rows]
        print('new_rows',new_rows)
        new_rows.insert(0, [force_text(c.text) for c in context['result_headers'].cells ])
        return new_rows
    def get_xls_export(self, context):
        datas = self._get_datas(context)
        print('formdata',self.formdata(datas))
        return self.formdata(datas)
        # output = io.BytesIO()
        # export_header = (
        #     self.request.GET.get('export_xls_header', 'off') == 'on')
        # export_temp = (
        #         self.request.GET.get('export_xls_temp', 'off') == 'on')

        # print('export_temp111111111', export_temp)
        model_name = self.opts.verbose_name
        # book = xlwt.Workbook(encoding='utf8')
        # sheet = book.add_sheet(
        #     u"%s %s" % (_(u'Sheet'), force_text(model_name)))
        blankrownum = 0
        d2=[]
        if 1==1:
            # 获取模板
            datas,replacedata,msg=self.formdata(datas)
            print('msg',msg)
            if msg['code'] =='err':
                return msg
            d1,d2=self.fileload(replacedata=replacedata)
            print('d1',d1)
            print('d2',d2)
            blankrownum = 5
            from xlrd import open_workbook
            from xlutils.copy import copy
            rb = open_workbook("./Template.xls", formatting_info=True)

            # sheet = rb.sheet_by_index(0)
            book = copy(rb)
            sheet =book.get_sheet(0)
            # sheet = book.sheet_by_index(0)
            #计算更新模板中的变量参数 {'_name_':'姓名','_month_':'3','_lilv_':'500'} 2018年4月30日
            # sheet的名称，行数，列数
            print('sheet',sheet.__dict__)
            print('rb',rb.__dict__)
            print(sheet.name, sheet._Worksheet__cols, sheet._Worksheet__rows)
            for x in sheet._Worksheet__rows:
                print('x',type(x))
            # for x in range(0,blankrownum):
            #     for y in range(0,7):
            #         cell_value = sheet.cell_value(x, y).encode('utf-8')
            #         if cell_value:
            #             print('cell_value',cell_value)

        styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                  'date': xlwt.easyxf(num_format_str='dd/mm/yyyy'),
                  'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                  'header': xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00'),
                  'default': xlwt.Style.default_style}

        if not export_header:
            datas = datas[1:]
        maxrowx = 0
        maxcolx = 0
        for rowx, row in enumerate(datas):
            for colx, value in enumerate(row):
                if export_header and rowx == 0:
                    cell_style = styles['header']
                else:
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    elif isinstance(value, datetime.date):
                        cell_style = styles['date']
                    elif isinstance(value, datetime.time):
                        cell_style = styles['time']
                    else:
                        cell_style = styles['default']
                print(rowx,colx,len(d2),'d2d2d2d2',d2)
                if len(d2)>0 and rowx<=len(d2) and colx<len(d2[0]):
                    print('d2[rowx][colx]',d2[rowx][colx])
                    if d2[rowx][colx]:
                        sheet.write(rowx, colx, d2[rowx][colx], style=cell_style)
                sheet.write(rowx+blankrownum, colx, value, style=cell_style)
                maxrowx = rowx+blankrownum
                maxcolx = colx -1
        if blankrownum>0:
            today = datetime.datetime.now()
            formatted_today = str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日'
            sheet.write(maxrowx + 1, maxcolx-1, formatted_today, style=cell_style)
            sheet.write(maxrowx + 2, maxcolx-1, '盖章', style=cell_style)
        book.save(output)

        output.seek(0)
        return output.getvalue()


    def get_response(self, response, context, *args, **kwargs):
        file_type = self.request.GET.get('print', 'false')
        # response = HttpResponse(
        #     content_type="%s; charset=UTF-8" % 'csv')
        #
        # file_name = self.opts.verbose_name.replace(' ', '_')
        # response['Content-Disposition'] = ('attachment; filename=%s.%s' % (
        #     file_name, 'csv')).encode('utf-8')
        #
        # response.write(getattr(self, 'get_%s_export' % 'xls')(context))
        # return response
        if file_type=='false':
            return response
        else:
            # self.get_xls_export(context)
            datas = self._get_datas(context)
            datas, replacedata, msg = self.formdata(datas)
            print('msg', msg)
            today = datetime.datetime.now()
            formatted_today = str(today.year) + '年' + str(today.month) + '月' + str(today.day) + '日'
            # if msg['code'] == 'err':
            #     return msg
            return render(response, 'print_card.html', {"formatted_today":formatted_today,"datas": datas, 'name': replacedata['_name_'], 'month': replacedata['_month_'], 'lilv': replacedata['_lilv_'],'msg':msg['msg']})

site.register_plugin(ExportMenuPlugin1, ListAdminView)

# site.register_plugin(ExportPlugin1, ListAdminView)
