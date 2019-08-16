from django import template
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import models, transaction
from django.urls.base import reverse, NoReverseMatch
from django.forms.models import modelform_factory
from django.forms import Media
from django.http import Http404, HttpResponse
from django.utils.encoding import force_text, smart_text
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from xadmin.plugins.ajax import JsonErrorDict
from xadmin.sites import site
from xadmin.util import lookup_field, display_for_field, label_for_field, unquote, boolean_icon
from xadmin.views import BaseAdminPlugin, ModelFormAdminView, ListAdminView
from xadmin.views.base import csrf_protect_m, filter_hook
from xadmin.views.edit import ModelFormAdminUtil
from xadmin.views.list import EMPTY_CHANGELIST_VALUE
from xadmin.layout import FormHelper


class DetailablePlugin(BaseAdminPlugin):

    detailitem = []
    show_all_rel_details = True

    def __init__(self, admin_view):
        super(DetailablePlugin, self).__init__(admin_view)
        self.printable_need_fields = {}
        self.mylist=[]

    def init_request(self, *args, **kwargs):
        print('1212121',self.detailitem)
        active = bool(self.request.method == 'GET' and self.detailitem)
        print('detailitem active',active,self.detailitem)
        if active:
            self.model_form = self.get_model_view(ModelFormAdminUtil, self.model).form_obj
        return active

    def result_item(self, item, obj, field_name, row):
        if (self.show_all_rel_details or (field_name in self.detailitem)):
            rel_obj = None
            if hasattr(item.field, 'remote_field') and isinstance(item.field.remote_field, models.ManyToOneRel):
                rel_obj = getattr(obj, field_name)
            elif field_name in self.detailitem:
                rel_obj = obj

            if rel_obj:
                if rel_obj.__class__ in site._registry:
                    try:
                        model_admin = site._registry[rel_obj.__class__]
                        has_view_perm = model_admin(self.admin_view.request).has_view_permission(rel_obj)
                        has_change_perm = model_admin(self.admin_view.request).has_change_permission(rel_obj)
                    except:
                        has_view_perm = self.admin_view.has_model_perm(rel_obj.__class__, 'view')
                        has_change_perm = self.has_model_perm(rel_obj.__class__, 'change')
                else:
                    has_view_perm = self.admin_view.has_model_perm(rel_obj.__class__, 'view')
                    has_change_perm = self.has_model_perm(rel_obj.__class__, 'change')

            if rel_obj and has_view_perm:
                print('typeof rel_obj',rel_obj,type(rel_obj),self.mylist)
                if rel_obj in self.mylist:
                    print(rel_obj,'已在列表,返回')
                    return item
                opts = rel_obj._meta
                try:
                    item_res_uri = reverse(
                        '%s:%s_%s_details' % (self.admin_site.app_name,
                                             opts.app_label, opts.model_name),
                        args=(getattr(rel_obj, opts.pk.attname),))

                    if item_res_uri:
                        if has_change_perm:
                            edit_url = reverse(
                                '%s:%s_%s_change' % (self.admin_site.app_name, opts.app_label, opts.model_name),
                                args=(getattr(rel_obj, opts.pk.attname),))
                        else:
                            edit_url = ''
                        self.mylist.append(rel_obj)
                        tmphtml = ('<a data-res-uri="%s" data-edit-uri="%s" class="details-handler" rel="tooltip" title="%s">详情<i class="fa fa-info-circle"></i></a>'
                                         % (item_res_uri, edit_url, _(u'Details of %s') % str(rel_obj)))
                        if tmphtml in item.btns:
                            print('按钮已有')
                        else:
                            item.btns.append(tmphtml)
                        print('item.btns',item.btns)
                except NoReverseMatch:
                    pass
        return item

    # Media
    def get_media(self, media):
        # if self.printable_need_fields:

        try:
            m = self.model_form.media
        except:
            m = Media()
        media = media + m +\
            self.vendor(
                'xadmin.plugin.details.js', 'xadmin.widget.details.css')
        return media


class EditPatchView(ModelFormAdminView, ListAdminView):

    def init_request(self, object_id, *args, **kwargs):
        self.org_obj = self.get_object(unquote(object_id))

        # For list view get new field display html
        self.pk_attname = self.opts.pk.attname

        if not self.has_change_permission(self.org_obj):
            raise PermissionDenied

        if self.org_obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') %
                          {'name': force_text(self.opts.verbose_name), 'key': escape(object_id)})

    def get_new_field_html(self, f):
        result = self.result_item(self.org_obj, f, {'is_display_first':
                                                    False, 'object': self.org_obj})
        return mark_safe(result.text) if result.allow_tags else conditional_escape(result.text)

    def _get_new_field_html(self, field_name):
        try:
            f, attr, value = lookup_field(field_name, self.org_obj, self)
        except (AttributeError, ObjectDoesNotExist):
            return EMPTY_CHANGELIST_VALUE
        else:
            allow_tags = False
            if f is None:
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                if boolean:
                    allow_tags = True
                    text = boolean_icon(value)
                else:
                    text = smart_text(value)
            else:
                if isinstance(f.rel, models.ManyToOneRel):
                    field_val = getattr(self.org_obj, f.name)
                    if field_val is None:
                        text = EMPTY_CHANGELIST_VALUE
                    else:
                        text = field_val
                else:
                    text = display_for_field(value, f)
            return mark_safe(text) if allow_tags else conditional_escape(text)

    @filter_hook
    def get(self, request, object_id):
        model_fields = [f.name for f in self.opts.fields]
        fields = [f for f in request.GET['fields'].split(',') if f in model_fields]
        defaults = {
            "form": self.form,
            "fields": fields,
            "formfield_callback": self.formfield_for_dbfield,
        }
        form_class = modelform_factory(self.model, **defaults)
        form = form_class(instance=self.org_obj)

        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        form.helper = helper

        s = '{% load i18n crispy_forms_tags %}<form method="post" action="{{action_url}}">{% crispy form %}' + \
            '<button type="submit" class="btn btn-success btn-block btn-sm">{% trans "Apply" %}</button></form>'
        t = template.Template(s)
        c = template.Context({'form': form, 'action_url': self.model_admin_url('patch', self.org_obj.pk)})

        return HttpResponse(t.render(c))

    @filter_hook
    @csrf_protect_m
    @transaction.atomic
    def post(self, request, object_id):
        model_fields = [f.name for f in self.opts.fields]
        fields = [f for f in request.POST.keys() if f in model_fields]
        defaults = {
            "form": self.form,
            "fields": fields,
            "formfield_callback": self.formfield_for_dbfield,
        }
        form_class = modelform_factory(self.model, **defaults)
        form = form_class(
            instance=self.org_obj, data=request.POST, files=request.FILES)

        result = {}
        if form.is_valid():
            form.save(commit=True)
            result['result'] = 'success'
            result['new_data'] = form.cleaned_data
            result['new_html'] = dict(
                [(f, self.get_new_field_html(f)) for f in fields])
        else:
            result['result'] = 'error'
            result['errors'] = JsonErrorDict(form.errors, form).as_json()

        return self.render_response(result)


site.register_plugin(DetailablePlugin, ListAdminView)
site.register_modelview(r'^(.+)/patch/$', EditPatchView, name='%s_%s_patch')
