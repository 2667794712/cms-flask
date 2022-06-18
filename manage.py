from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps.cms import models as cms_models
from apps.front.models import FrontUser
from bbs import create_app
from exts import db
from apps.models import BannerModel
from apps.models import BoardModel

CMSUser = cms_models.CMSUser
app = create_app()

manager = Manager(app)

Migrate(app, db)  # 绑定app跟db
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
