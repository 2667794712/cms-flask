from flask import Blueprint, views, render_template, request, session, jsonify, g
from flask import url_for, redirect

import config
from apps.models import BoardModel
from exts import db
from utils import restful, xjson
from .decorators import login_required
from .forms import LoginForm, AddBannerForm, UpdateBannerForm, ResetpwdForm
from .models import CMSUser
from ..models import BannerModel

bp = Blueprint("cms", __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

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
                    # 31天后过期
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='用户名或密码错误')

        else:
            # form.errors的错误信息格式，是一个字典，value是列表的形式
            # {'email': ['请输入正确的邮箱格式'], 'password': ['密码长度不够或超出']}
            message = form.errors.popitem()[1][0]
            return self.get(message=message)


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/', )
@login_required
def profile():
    return render_template('cms/cms_profile.html')


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        resetpwd_form = ResetpwdForm(request.form)
        if resetpwd_form.validate():
            oldpwd = resetpwd_form.oldpwd.data
            newpwd = resetpwd_form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 因为接受的是ajax,所以这里使用jsonify返回数据
                # 返回code字段表示状态码，message信息提示
                return jsonify({"code": 200, "message": "修改成功"})
            else:
                return jsonify({"code": 400, "message": "原密码错误"})
        else:
            message = resetpwd_form.get_error()
            return jsonify({"code": 400, "message": message})


bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))


# 轮播图
@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return xjson.json_success()
    else:
        return xjson.json_param_error(message=form.get_error())


@bp.route('/ubanner/', methods=['POST'])
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.img_url = img_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图')
    else:
        return restful.params_error(message=form.get_error())


# 板块管理
@bp.route('/boards/')
@login_required
def boards():
    all_boards = BoardModel.query.all()
    context = {
        'boards': all_boards
    }
    return render_template('cms/cms_boards.html', **context)


# @bp.route('/uboard/', methods=['POST'])
# @login_required
# def uboard():
#     update_board_form = UpdateBoardForm(request.form)
#     if update_board_form.validate():
#         board_id = update_board_form.board_id.data
#         name = update_board_form.name.data
#         if board_id:
#             board = BoardModel.query.get(board_id)
#             board.name = name
#             db.session.commit()
#             return xjson.json_success(message='更新成功')
#         else:
#             return xjson.json_param_error(message='板块不存在')
#     else:
#         return xjson.json_param_error(message=update_board_form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return xjson.json_param_error(message='请传入板块id')
    board = BoardModel.query.get(board_id)
    if not board:
        return xjson.json_param_error(message='没有这个板块')
    db.session.delete(board)
    db.session.commit()
    return xjson.json_success(message='删除板块成功')
