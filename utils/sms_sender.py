# encoding: utf-8
import requests


def send(mobile,sms_captcha):
    url = 'http://v.juhe.cn/sms/send'
    params = {
        'mobile':mobile,
        'tpl_id':'176407',
        'tpl_value':'#code#='+sms_captcha,
        'key':'bea49891fc6a193bb8dbef3469419311'
    }
    resp = requests.get(url,params=params)
    result = resp.json()
    if result['error_code'] == 0:
        return True
    else:
        return False
