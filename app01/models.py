from django.db import models
from django.utils import timezone

# Create your models here.
# 操作数据库
# 一个类就是一张表
# python manage.py makemigrations
# python manage.py migrate
# 班级表


class Class(models.Model):
    # 班级名称
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    # 主键id 自动生成一个字段， 自增， 主键
    number = models.CharField(max_length=30)
    name = models.CharField(max_length=30)  # max_length是字段的最大长度
    age = models.IntegerField()  # default是默认值
    score = models.DecimalField(max_digits=5, decimal_places=2)  # 最大位数和小数位数
    email = models.EmailField(max_length=100)  # django自带验证功能
    date_add = models.DateTimeField(auto_now_add=True)   # auto_now_add=True自动添加当前时间
    # 外键（ForeignKey）与班级建立关系
    # CASCADE：级联操作。如果外键对应的那条数据被删除了，那么这条数据也会被删除
    cls = models.ForeignKey('Class', on_delete=models.CASCADE, null=True)
    # 添加头像,存储的是图片路径
    # django后台上传文件路径
    # ImageField需要安装模块   pip install Pillow
    avatar = models.ImageField(max_length='100', upload_to='avatar/', default='avatar.jpg')

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name 字段在Django admin控制台显示的表名
        verbose_name = '学生管理'
        # verbose_name_plural 字段在Django admin控制台显示的表名的复数形式不加s,默认加s
        verbose_name_plural = verbose_name


class User(models.Model):
    # 自增主键id ,自动创建
    """用户表"""
    GENDER_CHOICE = (
        ('male', '男'),    # 第一次会存储到数据库中
        ('female', '女'),
    )
    # null=True表示数据库中可以为空，
    # blank=True表示django自带的后台可以为空
    name = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=20)
    hash_password = models.CharField('哈希密码', max_length=128, null=True, blank=True)
    gender = models.CharField('性别', choices=GENDER_CHOICE, max_length=10, default=GENDER_CHOICE[0][1])   # 性别
    email = models.CharField('邮箱', max_length=100, unique=True)
    # phone = models.CharField('电话',max_length=11)
    register_time = models.DateTimeField('注册日期', default=timezone.now) # 注册时间
    # last_login_time # 最后登录时间
    # is_active

    def __str__(self):
        # 默认《class int》，重写此方法可以在调式的时候看到示例
        return '<class user>{}'.format(self.name)



