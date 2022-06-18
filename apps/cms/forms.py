# cmd/forms.py

from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),
                                    InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='密码长度不够或超出')])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message="两次输入的密码不一致")])
