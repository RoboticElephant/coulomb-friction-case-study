from flask_smorest import Blueprint


blp = Blueprint("world", __name__, description="This is the route location")


@blp.route("/")
def hello():
    return "Welcome to Tenaris Case Study on Coulomb Friction by Josh Blakely"
    # fig = Figure()
    # ax = fig.subplots()
    # ax.plot([1, 2])
    #
    # buf = BytesIO()
    # fig.savefig(buf, format='png')
    #
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/> <br> <img src='data:image/png;base64,{data}'/>"
