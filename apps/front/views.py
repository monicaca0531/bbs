# encoding: utf-8

from flask import Blueprint, views, render_template, request,make_response, session, g, abort
from utils import restful,safeutils
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from .models import FrontUser
from exts import db
import config
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func


bp = Blueprint("front",__name__)


@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int)
    sort = request.args.get('st',type=int)
    banners = BannerModel.query.order_by(BannerModel.priority).all()[0:4]
    boards = BoardModel.query.all()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    total = 0
    obj_query = PostModel.query
    if sort == 1:
        obj_query = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        ## 加精的时间倒序
        obj_query = db.session.query(PostModel).outerjoin(HighlightModel).order_by(
            HighlightModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        ## 点赞最多
        obj_query = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        ## 评论最多
        obj_query = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(
            CommentModel.id),PostModel.create_time.desc())

    if board_id:
        obj_query = obj_query.filter(PostModel.board_id==board_id)
    #     posts = obj_query.slice(start,end)
    #     total = obj_query.count()
    # else:
    #     posts = obj_query.slice(start,end)
    #     total = obj_query.count()
    posts = obj_query.slice(start, end)
    total = obj_query.count()

    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0)
    context = {
        "banners": banners,
        "boards":boards,
        "posts":posts,
        "pagination":pagination,
        "current_board":board_id,
        "current_sort":sort
    }
    return render_template('front/front_index.html',**context)


@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html',post=post)


@bp.route('/acomment/',methods=['POST'])
@login_required
def acomment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if not post:
            abort(404)
        comment = CommentModel(content=content,post_id=post_id)
        comment.author = g.front_user
        db.session.add(comment)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/apost/',methods=['POST','GET'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error('没有该模板')
            post = PostModel(title=title,content=content,board_id=board_id)
            db.session.add(post)
            post.author = g.front_user
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')
    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password1.data
            username = form.username.data
            exists = FrontUser.query.filter_by(telephone=telephone).first()
            if exists:
                return restful.unauth_error('该号码已被注册')
            else:
                user = FrontUser(telephone=telephone,username=username,password=password)
                db.session.add(user)
                db.session.commit()
                return restful.success()
        else:
            message = form.get_error()
            print(message)
            return restful.params_error(message)


class SigninView(views.MethodView):
    def get(self):
        return render_template('front/front_signin.html')
    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error('手机号码或密码错误')
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))

