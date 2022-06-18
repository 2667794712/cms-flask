from flask import Blueprint, views, render_template, request, session
from flask import url_for, redirect
from .forms import LoginForm
from .models import CMSUser
from .decorators import login_required
import config

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


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        pass


bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
