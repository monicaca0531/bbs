# encoding: utf-8

from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp, Length, InputRequired
import hashlib


class SMSCaptchaForm(BaseForm):
    salt = 'ssadhiuyweghaneiopqh!jdie#d@~`'
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}',message='手机号码格式有误')])
    timestamp = StringField(validators=[Length(13,13)])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        sign2 = hashlib.md5((telephone+timestamp+self.salt).encode('utf-8')).hexdigest()
        print('sign:',sign)
        print('sign:',sign2)

        if sign2 == sign:
            return True
        else:
            return False