from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired
from ..forms import BaseForm


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请选择版块')])
