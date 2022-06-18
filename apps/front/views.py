from io import BytesIO

from flask import (
    Blueprint,
    views,
    render_template,
    make_response,
    request
)

from apps.models import BannerModel, BoardModel
from utils import Captcha, restful

bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    context = {
        'banners': banners,
        'boards': boards
    }
    return render_template('front/front_index.html', **context)


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')  # 指定格式为png
    out.seek(0)  # 把指针指到开始位置
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/apost/')
def apost():
    return render_template('front/front_apost.html')
