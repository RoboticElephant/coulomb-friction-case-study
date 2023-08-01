import logging_config
import logging
import os

from flask import Flask, jsonify
from flask_smorest import Api
# from flask_jwt_extended import JWTManager

logger = logging.getLogger(__name__)

from db import db
import models
# from blocklist import BLOCKLIST

from resources.world import blp as WorldBlueprint
from resources.friction import blp as FrictionBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    # Title of the API
    app.config["API_TITLE"] = "Tenaris Case Study REST API"
    # Version
    app.config["API_VERSION"] = "v1"
    # OpenAPI Version
    app.config["OPENAPI_VERSION"] = "3.0.3"
    # Where is the root of the API
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # Use swagger for the API implementation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # Where the code is to be used
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # The DATABASE_URL allows us to save it outside our code if it exists
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    # Will create the table(s) if they don't exist otherwise skip this if they do.
    with app.app_context():
        db.create_all()

    # # This is the secret key that makes sure the user hasn't created their own
    # # This should be stored as an environment variable.
    # # What we can do is run secrets.SystemRandom().getrandbits(128) to create the secret that would be used here
    # app.config["JWT_SECRET_KEY"] = "josh"  # TODO this will just be temporary for now
    # jwt = JWTManager(app)
    #
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     return jwt_payload["jti"] in BLOCKLIST
    #
    # @jwt.revoked_token_loader
    # def revoked_token_callback(jwt_header, jwt_payload):
    #     return jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401
    #
    # @jwt.needs_fresh_token_loader
    # def token_not_fresh_callback(jwt_header, jwt_payload):
    #     return jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), 401
    #
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     # This current implementation isn't ideal. Should see whether the user is an admin by looking at a database.
    #     if identity == 1:
    #         return {"is_admin": True}
    #     else:
    #         return {"is_admin": False}
    #
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401
    #
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401
    #
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401

    api.register_blueprint(WorldBlueprint)
    api.register_blueprint(FrictionBlueprint)
    return app


if __name__ == "__main__":
    create_app()

# @app.route("/")
# def hello():
#     fig = Figure()
#     ax = fig.subplots()
#     ax.plot([1, 2])
#
#     buf = BytesIO()
#     fig.savefig(buf, format='png')
#
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     return f"<img src='data:image/png;base64,{data}'/> <br> <img src='data:image/png;base64,{data}'/>"