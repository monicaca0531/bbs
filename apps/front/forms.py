# encoding: utf-8

from apps.forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired
from utils import bbscache

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}',message='请输入正确格式的电话号码')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}',message='请输入正确的验证码')])
    username = StringField(validators=[Regexp(r".{2,20}",message='请输入2到20位的用户名')])
    password1 = StringField(validators=[Regexp(r".{6,18}",message='请输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo("password1",message='重复密码与设置密码不一致')])
    img_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确的验证码')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_mem = bbscache.get(telephone)
        if not sms_captcha_mem or sms_captcha.lower() != sms_captcha_mem:
            raise ValidationError('短信验证码不正确')

    def validate_img_captcha(self,field):
        telephone = self.telephone.data
        username = self.username.data
        password1 = self.password1.data
        password2 = self.password2.data
        print(telephone,'*',username,'*',password1,'*',password2)
        img_captcha = field.data
        img_captcha_mem = bbscache.get(img_captcha.lower())
        if not img_captcha_mem:
            raise ValidationError('图片验证码不正确')


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确格式的电话号码')])
    password = StringField(validators=[Regexp(r".{6,18}", message='请输入正确格式的密码')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='必须输入标题')])
    content = StringField(validators=[InputRequired(message='必须输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='必须输入模板id')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id = IntegerField(validators=[InputRequired(message='请传入帖子id')])