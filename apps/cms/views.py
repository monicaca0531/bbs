# encoding: utf-8

from flask import Blueprint,views,render_template,request,redirect,url_for,session, g
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, UpdateBoardForm
from .models import CMSUser,CMSPermision
import config
from .decorators import login_required,permision_required
from utils import restful, bbscache
from exts import db, mail
from flask_mail import Message
import string
import random
from apps.models import BannerModel, BoardModel, PostModel, HighlightModel
from tasks import send_mail


bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
@login_required
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error(message='请输入邮箱')
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha = "".join(random.sample(source,6))

    # message = Message('Python验证码',recipients=['635867032@qq.com'],body='您的邮箱验证码为：%s' % captcha)
    send_mail('Python验证码',recipients=['635867032@qq.com'],body='您的邮箱验证码为：%s' % captcha)
    bbscache.set(email,captcha)
    return restful.success()
    # try:
    #     mail.send(message)
    #     return restful.success()
    # except:
    #     return restful.server_error()


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


@bp.route('/abanner/',methods=['POST'])
@login_required
def addbanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        img_url = form.img_url.data
        link_to = form.link_to.data
        priority = form.priority.data
        banner = BannerModel(name=name, img_url=img_url, link_to=link_to, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def updatebanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        img_url = form.img_url.data
        link_to = form.link_to.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.img_url = img_url
            banner.link_to = link_to
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这个轮播图')
    else:
        return restful.params_error(form.get_error())


@bp.route('/dbanner/',methods=['POST'])
@login_required
def deletebanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error('没有这个轮播图')
    banner = BannerModel.query.get(banner_id)
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/posts/')
@login_required
@permision_required(CMSPermision.POSTER)
def posts():
    context = {
        "posts":PostModel.query.order_by(PostModel.create_time.desc()).all()[1:11]
    }
    return render_template('cms/cms_posts.html',**context)


@bp.route('/dposts/',methods=['POST'])
@login_required
@permision_required(CMSPermision.POSTER)
def dposts():
    post_id = request.form.get("post_id")
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')
    db.session.delete(post)
    db.session.commit()
    return restful.success()


@bp.route('/hposts/',methods=['POST'])
@login_required
@permision_required(CMSPermision.POSTER)
def hposts():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')
    highlight = HighlightModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/dhposts/',methods=['POST'])
@login_required
@permision_required(CMSPermision.POSTER)
def dhposts():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('没有这篇帖子')
    highlight = HighlightModel.query.filter_by(post_id=post_id).first()
    print(highlight.id)
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permision_required(CMSPermision.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permision_required(CMSPermision.BOARDER)
def boards():
    boards = BoardModel.query.all()
    context = {
        'boards':boards
    }
    return render_template('cms/cms_boards.html',**context)


@bp.route('/aboard/',methods=['POST'])
@login_required
@permision_required(CMSPermision.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        exist = BoardModel.query.filter_by(name=name).first()
        if exist:
            return restful.params_error('该模板名称已存在')
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())

@bp.route('/uboard/',methods=['POST'])
@login_required
@permision_required(CMSPermision.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if not board:
            return restful.params_error('该模板id不存在')
        board.name = name
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/dboard/',methods=['POST'])
@login_required
@permision_required(CMSPermision.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error('请传入模板id')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error('该模板id不存在')
    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_required
@permision_required(CMSPermision.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permision_required(CMSPermision.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permision_required(CMSPermision.ALL_PERMISION)
def croles():
    return render_template('cms/cms_croles.html')


class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或验证码错误')
        else:
            message = form.get_error()
            return self.get(message=message)


class Resetpwd(views.MethodView):
    decorators = [login_required,]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                print('2222222')
                return restful.params_error(message='旧密码错误')
        else:
            print('111')
            message = form.get_error()
            return restful.params_error(message=message)


class ResetEmail(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            newemail = form.newemail.data
            user = g.cms_user
            user.email = newemail
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=Resetpwd.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmail.as_view('resetemail'))

