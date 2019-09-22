# encoding: utf-8

from flask import Blueprint,make_response,url_for,request,jsonify
from utils.captcha import Captcha
from io import BytesIO
from utils import sms_sender,restful,bbscache
from .forms import SMSCaptchaForm
import qiniu
import config

bp = Blueprint("common",__name__,url_prefix='/c')

@bp.route('/graph_captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    bbscache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error('请输入手机号码')
#     captcha = Captcha.gene_text(number=4)
#     print(captcha)
#     # result = sms_sender.send(telephone,captcha)
#     # if result:
#     #     return restful.success()
#     # else:
#     #     return restful.params_error('发送验证码失败')
#     return restful.success()

@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print(captcha)
        # result = sms_sender.send(telephone,captcha)
        # if result:
        #     return restful.success()
        # else:
        #     return restful.params_error('发送验证码失败')
        if telephone and captcha:
            bbscache.set(telephone,captcha.lower())
            return restful.success()
        else:
            return restful.params_error('发送验证码失败')
    else:
        return restful.params_error('参数错误')


@bp.route('/uptoken/')
def uptoken():
    AccessKey = config.UEDITOR_QINIU_ACCESS_KEY
    SecretKey = config.UEDITOR_QINIU_SECRET_KEY
    bucket_name = config.UEDITOR_QINIU_BUCKET_NAME

    q = qiniu.Auth(AccessKey,SecretKey)
    token = q.upload_token(bucket=bucket_name)
    return jsonify({"uptoken":token})