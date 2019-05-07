from django.db import models
# from viewflow.models import Process
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

SERVER_STATUS = (
    (0, u"Normal"),
    (1, u"Down"),
    (2, u"No Connect"),
    (3, u"Error"),
)
SERVICE_TYPES = (
    ('moniter', u"Moniter"),
    ('lvs', u"LVS"),
    ('db', u"Database"),
    ('analysis', u"Analysis"),
    ('admin', u"Admin"),
    ('storge', u"Storge"),
    ('web', u"WEB"),
    ('email', u"Email"),
    ('mix', u"Mix"),
)

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        # name为上传文件名称
        import os, time, random
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)

@python_2_unicode_compatible
class IDC(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    contact = models.CharField(max_length=32)
    telphone = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    customer_id = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group)  # many

    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Host(models.Model):
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    nagios_name = models.CharField(u"Nagios Host ID", max_length=64, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    internal_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    ssh_port = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(choices=SERVER_STATUS)

    brand = models.CharField(max_length=64, choices=[(i, i) for i in (u"DELL", u"HP", u"Other")])
    model = models.CharField(max_length=64)
    cpu = models.CharField(max_length=64)
    core_num = models.SmallIntegerField(choices=[(i * 2, "%s Cores" % (i * 2)) for i in range(1, 15)])
    hard_disk = models.IntegerField()
    memory = models.IntegerField()

    system = models.CharField(u"System OS", max_length=32, choices=[(i, i) for i in (u"CentOS", u"FreeBSD", u"Ubuntu")])
    system_version = models.CharField(max_length=32)
    system_arch = models.CharField(max_length=32, choices=[(i, i) for i in (u"x86_64", u"i386")])

    create_time = models.DateField()
    guarantee_date = models.DateField()
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPES)
    description = models.TextField()

    administrator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Admin")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Host"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class MaintainLog(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    maintain_type = models.CharField(max_length=32)
    hard_type = models.CharField(max_length=16)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()

    def __str__(self):
        return '%s maintain-log [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
                                               self.maintain_type, self.hard_type)

    class Meta:
        verbose_name = u"Maintain Log"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class HostGroup(models.Model):

    name = models.CharField(max_length=32)
    description = models.TextField()
    hosts = models.ManyToManyField(
        Host, verbose_name=u'Hosts', blank=True, related_name='groups')

    class Meta:
        verbose_name = u"Host Group"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"Access Record"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s Access Record" % self.date.strftime('%Y-%m-%d')

@python_2_unicode_compatible
class kmChoices(models.Model):
  description = models.CharField(max_length=64)

  def __str__(self):
      return self.description

  class Meta:
      verbose_name = u"考试科目"
      verbose_name_plural = verbose_name


@python_2_unicode_compatible
class ccpa(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    area = models.CharField(max_length=64, verbose_name=u'报名地区')
    train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    periods = models.CharField(max_length=64, verbose_name=u'期数', choices=[(i, i) for i in (u"一期", u"二期", u"三期")])
    name = models.CharField(max_length=64, verbose_name=u'姓名')
    pinyin = models.CharField(max_length=64, verbose_name=u'姓名拼音')
    sex = models.CharField(max_length=64, verbose_name=u'性别', choices=[(i, i) for i in (u"男", u"女")])
    guarantee_date = models.DateField(verbose_name=u'出生日期')
    nation = models.CharField(max_length=16, verbose_name=u'民族')
    edu = models.CharField(max_length=64, verbose_name=u'学历', choices=[(i, i) for i in (u"本科", u"专科", u"硕士")])
    poilt = models.CharField(max_length=64, verbose_name=u'政治面貌', choices=[(i, i) for i in (u"群众", u"党员")])
    icc = models.CharField(max_length=64, verbose_name=u'身份证号')
    phone = models.CharField(max_length=20, verbose_name=u'手机号')
    email = models.EmailField(error_messages={'invalid': '格式错了.'}, verbose_name=u'联系邮箱')
    school = models.CharField(max_length=64, verbose_name=u'学校')
    specialty = models.CharField(max_length=64, verbose_name=u'专业')
    work = models.CharField(max_length=64, verbose_name=u'工作单位', blank=True, null=True)
    job = models.CharField(max_length=64, verbose_name=u'职务', blank=True, null=True)
    address = models.CharField(max_length=128, verbose_name=u'联系地址')
    enaddress = models.CharField(max_length=128, verbose_name=u'英文地址')
    Postcodes = models.CharField(max_length=16, verbose_name=u'邮编')
    telephone = models.CharField(max_length=16, verbose_name=u'电话')
    type = models.CharField(max_length=64, verbose_name=u'报考类型', choices=[(i, i) for i in (u"CCPA初级", u"CCPA中级", u"CCPA高级")])
    kskm = models.ManyToManyField(kmChoices, verbose_name=u'考试科目')
    exam_date = models.DateField(verbose_name=u'考试时间')
    exam_address = models.CharField(max_length=128, verbose_name=u'考试地点')
    photo = models.ImageField(upload_to='upload/image/%Y/%m',storage=ImageStorage(), max_length=100, verbose_name=u'上传照片', null=True, blank=True, )
    status = models.CharField(max_length=64,verbose_name=u'报名状态', choices=[(i, i) for i in (u"草稿", u"通过")], default='草稿')
    # card_no = models.CharField(max_length=64, verbose_name=u'准考证号')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='最近修改时间', auto_now=True)
    def get_card_no(self):
        school_no = str(self.train.id).zfill(3)
        # bmyearm = self.create_date.strftime("1%m")
        # print('bmyearm', bmyearm)
        card_no = school_no + '1' + str(self.id).zfill(6)

        return card_no

    get_card_no.short_description = "准考证号"
    card_no = property(get_card_no)
    def __str__(self):
        return self.name

    def get_card_no(self):
        return self.id

    class Meta:
        verbose_name = u"CCPA项目"
        verbose_name_plural = verbose_name




@python_2_unicode_compatible
class xss(models.Model):
    model_name = 'xss'
    # UPLOAD_PATH_IMAGE = 'upload/image/'
    area = models.CharField(max_length=64, verbose_name=u'报名地区')
    train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    periods = models.CharField(max_length=64, verbose_name=u'期数', choices=[(i, i) for i in (u"一期", u"二期", u"三期")])
    name = models.CharField(max_length=64, verbose_name=u'姓名')
    pinyin = models.CharField(max_length=64, verbose_name=u'姓名拼音')
    sex = models.CharField(max_length=64, verbose_name=u'性别', choices=[(i, i) for i in (u"男", u"女")])
    guarantee_date = models.DateField(verbose_name=u'出生日期')
    nation = models.CharField(max_length=16, verbose_name=u'民族')
    edu = models.CharField(max_length=64, verbose_name=u'学历', choices=[(i, i) for i in (u"本科", u"专科", u"硕士")])
    poilt = models.CharField(max_length=64, verbose_name=u'政治面貌', choices=[(i, i) for i in (u"群众", u"党员")])
    icc = models.CharField(max_length=64, verbose_name=u'身份证号')
    phone = models.CharField(max_length=20, verbose_name=u'手机号')
    email = models.EmailField(error_messages={'invalid': '格式错了.'}, verbose_name=u'联系邮箱')
    # school = models.CharField(max_length=64, verbose_name=u'学校')
    # specialty = models.CharField(max_length=64, verbose_name=u'专业')
    work = models.CharField(max_length=64, verbose_name=u'工作单位', blank=True, null=True)
    job = models.CharField(max_length=64, verbose_name=u'职务', blank=True, null=True)
    address = models.CharField(max_length=128, verbose_name=u'联系地址')
    enaddress = models.CharField(max_length=128, verbose_name=u'英文地址')
    Postcodes = models.CharField(max_length=16, verbose_name=u'邮编')
    telephone = models.CharField(max_length=16, verbose_name=u'电话')
    type = models.CharField(max_length=64, verbose_name=u'报名类型', choices=[(i, i) for i in (u"CCPA《薪税师》一级", u"CCPA《薪税师》二级", u"CCPA《薪税师》三级")])
    # kskm = models.ManyToManyField(kmChoices, verbose_name=u'考试科目')
    below_date = models.DateField(verbose_name=u'线下授课时间')
    exam_date = models.DateField(verbose_name=u'考试时间')
    exam_address = models.CharField(max_length=128, verbose_name=u'考试地点')
    photo = models.ImageField(upload_to='upload/image/%Y/%m',storage=ImageStorage(), max_length=100, verbose_name=u'上传照片', null=True, blank=True, )

    status = models.CharField(max_length=64,verbose_name=u'报名状态', choices=[(i, i) for i in (u"草稿", u"通过")], default='草稿')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='最近修改时间', auto_now=True)
    # card_no = models.CharField(max_length=64, verbose_name=u'准考证号')
    def get_card_no(self):
        school_no = str(self.train.id).zfill(3)
        # bmyearm = self.create_date.strftime("2%m")
        # print('bmyearm',bmyearm)
        card_no =school_no+ '2'+str(self.id).zfill(6)

        return card_no

    get_card_no.short_description = "准考证号"
    card_no = property(get_card_no)
    # card_no.setter(verbose_name='准考证号')

    def __str__(self):
        return self.name

    # def clean_fields(self, exclude=None):


    # class Meta:


    class Meta:
        verbose_name = u"薪税师项目"
        # model_name = 'xss'
        verbose_name_plural = verbose_name
        # swappable = 'AUTH_USER_MODEL'

        # permissions = (
        #     ("change_xss_status", "Can change the status of xss"),
        # )


@python_2_unicode_compatible
class fund(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class treatment_item(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class customer(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    first_name = models.CharField(max_length=64)
    # train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField(verbose_name=u'birthday')
    contact_number = models.CharField(max_length=20)
    health_fund = models.ForeignKey(fund, on_delete=models.CASCADE,blank=True, null=True)
    health_fund_number = models.CharField(max_length=64,blank=True, null=True)


    def __str__(self):
        return self.first_name+' '+self.last_name

    def fullname(self):
        return self.first_name+' '+self.last_name

    # def get_card_no(self):
    #     return self.id

    class Meta:
        verbose_name = u"customer"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class provider(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    first_name = models.CharField(max_length=64)
    # train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    last_name = models.CharField(max_length=64)
    # contact_number = models.CharField(max_length=20)
    health_fund = models.ForeignKey(fund, on_delete=models.CASCADE)
    health_fund_number = models.CharField(max_length=64,verbose_name=u'provider number')

    def __str__(self):
        return self.first_name+' '+self.last_name+' '+str(self.health_fund)
    def fullname(self):
        return self.first_name+' '+self.last_name

    # def get_card_no(self):
    #     return self.id

    class Meta:
        verbose_name = u"provider"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class treatment(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    cust = models.ForeignKey(customer, on_delete=models.CASCADE, verbose_name="customer")
    date = models.DateTimeField( auto_now_add=True)#,input_formats=['%d/%m/%Y  %H:%M:%S','%d/%m/%Y  %H:%M:%S',
    # train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    item = models.ForeignKey(treatment_item, on_delete=models.CASCADE)

    prov = models.ForeignKey(provider, on_delete=models.CASCADE, verbose_name="provider")
    # contact_number = models.CharField(max_length=20)
    hicaps = models.DecimalField(max_digits=10, decimal_places=2)
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    minute = models.IntegerField()

    def __str__(self):
        return str(self.id)#+' '+self.last_name

    def cost(self):
        return str(self.hicaps+self.cash)

    class Meta:
        verbose_name = u"treatment"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class groupinfo(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    group_no = models.CharField(max_length=64,verbose_name=u'机构号')
    group_name = models.CharField(max_length=64,verbose_name=u'机构名')
    # train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")


    def __str__(self):
        return self.group_name
    def fullname(self):
        return self.group_no+' '+self.group_name


    # def get_card_no(self):
    #     return self.id

    class Meta:
        verbose_name = u"机构信息"
        verbose_name_plural = verbose_name
        unique_together = ('group_no',)


@python_2_unicode_compatible
class litreat(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    # cust = models.ForeignKey(customer, on_delete=models.CASCADE, verbose_name="customer")
    yearm = models.CharField(max_length=20, verbose_name="记录年月")#models.DateField( auto_now_add=False, verbose_name="记录年月")#
    icc_id = models.CharField(max_length=50, verbose_name="身份证号")
    nowm_acc = models.IntegerField(verbose_name="本月积分",default=0)
    all_acc = models.IntegerField(verbose_name="总积分/贡献度",default=0)
    con_num = models.CharField(max_length=50, verbose_name="账号")
    open_ins = models.CharField(max_length=50, verbose_name="开户机构",null=True,blank=True)
    open_no = models.CharField(max_length=50, verbose_name="开户机构号")
    # open_ins = models.ForeignKey(groupinfo, on_delete=models.CASCADE, verbose_name="开户机构")
    cust_name = models.CharField(max_length=20, verbose_name="客户名")
    jy_count = models.IntegerField(verbose_name="交易笔数",default=0)
    jy_num = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="交易金额",default=0)
    day_avg = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="日均",default=0)
    all_jy_count = models.IntegerField(verbose_name="总交易笔数",default=0)
    all_jy_num = models.DecimalField(max_digits=20, decimal_places=2,verbose_name="总交易金额",default=0.0)
    is_life = models.DecimalField(max_digits=20, decimal_places=2,verbose_name="百富生活圈折扣",default=9.6)#(default=False, verbose_name="百富生活圈折扣")
    jnlx_num = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="缴纳利息",default=0)
    is_show = models.BooleanField(default=False, verbose_name="是否展示易拉宝")
    is_ontime = models.BooleanField(default=False, verbose_name="是否按时还款")
    can_use_acc = models.IntegerField(verbose_name="可用积分",default=0)
    used_acc = models.IntegerField(verbose_name="本月消费积分",default=0)
    acc_detail = models.CharField(max_length=1204, verbose_name="积分消费详情",null=True,blank=True)
    is_quit = models.BooleanField(default=False, verbose_name="是否清退")
    is_bak = models.BooleanField(default=False, verbose_name="是否")
    # date = models.DateTimeField( auto_now_add=True)#,input_formats=['%d/%m/%Y  %H:%M:%S','%d/%m/%Y  %H:%M:%S',
    # train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    # item = models.ForeignKey(treatment_item, on_delete=models.CASCADE)

    # prov = models.ForeignKey(provider, on_delete=models.CASCADE, verbose_name="provider")

    def __str__(self):
        return str(self.id)#+' '+self.last_name

    def cost(self):
        #简单计算
        return str(self.nowm_acc+self.nowm_acc)

    class Meta:
        verbose_name = u"用户记录"
        verbose_name_plural = verbose_name
        unique_together = ('yearm','icc_id')



# @python_2_unicode_compatible
# class xsstest(Process):
#     # UPLOAD_PATH_IMAGE = 'upload/image/'
#     area = models.CharField(max_length=64, verbose_name=u'报名地区')
#     approved = models.BooleanField(default=False)