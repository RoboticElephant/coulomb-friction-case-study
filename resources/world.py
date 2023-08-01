from flask.views import MethodView
from flask_smorest import Blueprint

import base64
from io import BytesIO
from matplotlib.figure import Figure

blp = Blueprint("world", __name__, description="This is the route location")


@blp.route("/")
def hello():
    return "Hello World!"
    # fig = Figure()
    # ax = fig.subplots()
    # ax.plot([1, 2])
    #
    # buf = BytesIO()
    # fig.savefig(buf, format='png')
    #
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/> <br> <img src='data:image/png;base64,{data}'/>"
