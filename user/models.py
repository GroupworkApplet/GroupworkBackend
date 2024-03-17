from django.contrib.auth.models import User
from django.db import models


# 用户个人信息
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('0', '男'),
        ('1', '女'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=20)
    #email = models.EmailField(max_length=50, null=True, blank=True)
    password=models.CharField(max_length=15)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name="性别", default='0')
    birthday = models.CharField(max_length=20, verbose_name="生日时间", default="2000-1-1")
    def __str__(self):
        return self.user.username


# 教育或工作信息
class EducationOrWorkInfo(models.Model):
    COLLEGE_CHOICES = [
        ("0", "哲学学院"),
        ("1", "国学院"),
        ("2", "文学院"),
        ("3", "外国语言文学学院"),
        ("4", "新闻与传播学院"),
        ("5", "艺术学院"),
        ("6", "艺术教育中心"),
        ("7", "历史学院"),
        ("8", "经济与管理学院"),
        ("9", "法学院"),
        ("10", "马克思主义学院"),
        ("11", "社会学院"),
        ("12", "政治与公共管理学院"),
        ("13", "信息管理学院"),
        ("14", "数学与统计学院"),
        ("15", "物理科学与技术学院"),
        ("16", "化学与分子科学学院"),
        ("17", "生命科学学院"),
        ("18", "资源与环境科学学院"),
        ("19", "高等研究院"),
        ("20", "动力与机械学院"),
        ("21", "电气与自动化学院"),
        ("22", "城市设计学院"),
        ("23", "土木建筑工程学院"),
        ("24", "水利水电学院"),
        ("25", "工业科学研究院"),
        ("26", "水工程科学研究院"),
        ("27", "电子信息学院"),
        ("28", "计算机学院"),
        ("29", "测绘学院"),
        ("30", "遥感信息工程学院"),
        ("31", "国家网络安全学院"),
        ("32", "图像传播与印刷包装研究中心"),
        ("33", "医学部机关"),
        ("34", "医学研究院"),
        ("35", "基础医学院"),
        ("36", "公共卫生学院"),
        ("37", "药学院"),
        ("38", "护理学院"),
        ("39", "第一临床学院"),
        ("40", "第二临床学院"),
        ("41", "口腔医学院"),
        ("42", "医学职业技术学院"),
        ("43", "弘毅学堂"),
        ("44", "前沿交叉学科研究院"),
        ("45", "武汉数学与智能研究院"),
        ("46", "微电子学院")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education_or_work_info')
    school_or_company = models.CharField(max_length=50)
    major_or_department = models.CharField(max_length=50, choices=COLLEGE_CHOICES, default='0')
    class_or_position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.school_or_company}"


# 用户信用分
class UserCredit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credit')
    credit = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.user.username} - {self.credit}"
