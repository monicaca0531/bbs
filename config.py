# encoding: utf-8
import os

SECRET_KEY = os.urandom(24)

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'monicabbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'asdsaijjhfsa'
FRONT_USER_ID = 'sjhsjfkfba2iqyHJDjm,ks'

## 配置邮箱信息
## swjuoqzfbprrbbej

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '465'
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = 'monica0531@qq.com'
MAIL_PASSWORD = 'swjuoqzfbprrbbej'
MAIL_DEFAULT_SENDER = 'monica0531@qq.com'

# 七牛云配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "e2aQjMgC5t2W6YpnERfLhOM0eSOOZn21ZaCFZ-Ae"
UEDITOR_QINIU_SECRET_KEY = "wPJG_KgjX7KhgFpCHdUh9en6MMzjSxQSGCBiqgBp"
UEDITOR_QINIU_BUCKET_NAME = "underfire"
UEDITOR_QINIU_DOMAIN = "http://underfire.s3-cn-south-1.qiniucs.com/"

# 分页配置
PER_PAGE = 15


## 配置celery

CELERY_RESULT_BACKEND = "redis://:root@127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://:root@127.0.0.1:6379/0"

