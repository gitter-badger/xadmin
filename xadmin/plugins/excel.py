# _*_ coding:utf-8 _*_
from xadmin.plugins.utils import get_context_dict

__author__ = "yangtuo"
__date__ = "2019/4/3 21:12"

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    # 入口函数, 通过此属性来指定此字段是否加载此字段
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    # 如果加载, 则执行此函数添加一个 导入 字段
    def block_top_toolbar(self, context, nodes):
        nodes.append(
            loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context=get_context_dict(context)))



xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)