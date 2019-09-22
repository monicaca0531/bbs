# encoding: utf-8

from wtforms import StringField, IntegerField
from wtforms.validators import Email,InputRequired, Length, EqualTo, ValidationError,URL
from ..forms import BaseForm
from utils import bbscache
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式不正确'),InputRequired(message='必须填写邮箱')])
    password = StringField(validators=[Length(6,20,message='密码长度必须为6~20位'),InputRequired('必须输入密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='密码长度必须为6~20位'),InputRequired('必须输入密码')])
    newpwd = StringField(validators=[Length(6, 20, message='密码长度必须为6~20位'), InputRequired('必须输入密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='重复密码必须与新密码一致')])

class ResetEmailForm(BaseForm):
    newemail = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired('必须填写邮箱')])
    captcha = StringField(validators=[Length(6,6,message='请输入正确的验证码个数'),InputRequired('必须填写验证码')])

    def validate_captcha(self,field):
        captcha = field.data
        newemail = self.newemail.data
        captcha_cache = bbscache.get(newemail)
        print(captcha)
        print(captcha_cache)
        if not captcha_cache or captcha_cache.lower() != captcha.lower():
            raise ValidationError('验证码不正确')

    def validate_email(self,field):
        newemail = field.data
        user = g.cms_user
        if user.email == newemail:
            raise ValidationError('不能输入相同的邮箱')

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    img_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接'),URL()])
    link_to = StringField(validators=[InputRequired(message='请输入轮播图跳转链接'),URL()])
    priority = IntegerField(validators=[InputRequired(message='必须输入优先级')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired()])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入模板名称')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='必须传入id')])