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


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID')])


class AddBoardsForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入版块名称'), Length(2, 15, message='长度应在2-15个字符之间')])


class UpdateBoardForm(AddBoardsForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入版块名称')])
