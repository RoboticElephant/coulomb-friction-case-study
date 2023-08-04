from flask_smorest import Blueprint


blp = Blueprint("home", __name__, description="This is the route location")


@blp.route("/")
def welcome():
    return "Welcome to Tenaris Case Study on Coulomb Friction by Josh Blakely"
