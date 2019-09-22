# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from bbs import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightModel

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermision = cms_models.CMSPermision

FrontUser = front_models.FrontUser

app = create_app()
manager = Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('**cms用户创建成功**')

@manager.command
def create_role():
    # 1.访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者',desc='可以访问相关数据，但不能修改。')
    visitor.permisions = CMSPermision.VISITOR
    # 2.运营角色（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营人员',desc='管理帖子，管理评论，管理前台用户')
    operator.permisions = CMSPermision.VISITOR|CMSPermision.POSTER|CMSPermision.COMMENTER|CMSPermision.FRONTUSER\
                          |CMSPermision.BOARDER
    # 3.管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permisions = CMSPermision.VISITOR|CMSPermision.POSTER|CMSPermision.COMMENTER|CMSPermision.FRONTUSER\
                       |CMSPermision.CMSUSER|CMSPermision.BOARDER
    # 4.开发者（所有权限）
    developer = CMSRole(name='开发者',desc='开发人员专用角色')
    developer.permisions = CMSPermision.ALL_PERMISION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            print('该用户拥有 %s角色' % role.name)
        else:
            print('**没有此角色**')
    else:
        print('**没有此用户**')

@manager.command
def test_user_permision():
    user = CMSUser.query.first()
    if user.has_permision(CMSPermision.ADMINER):
        print('该用户拥有此权限')
    else:
        print('该用户没有此权限')

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-t','--telephone',dest='telephone')
def create_frontuser(username,password,telephone):
    user = FrontUser(username=username,password=password,telephone=telephone)
    db.session.add(user)
    db.session.commit()
    print('成功创建前台用户')

@manager.command
def create_test_posts():
    for i in range(1,6):
        title = '标题%s' %i
        content = '内容%s' %i
        author = FrontUser.query.first()
        board = BoardModel.query.get(3)
        post = PostModel(title=title,content=content)
        post.author = author
        post.board = board
        db.session.add(post)
        db.session.commit()
    print('创建完毕')

if __name__ == '__main__':
    manager.run()