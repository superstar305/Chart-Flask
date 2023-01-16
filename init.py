from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from config import Config
from API.schema import schema

from controller import api

def create_app(test_config=None):

	# creates an application that is named after the name of the file
	app = Flask(__name__)

	app.config.from_object(Config)

	cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

	# initializing routes
	app.add_url_rule(
		'/access',
		view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
	)
	app.register_blueprint(api.router, url_prefix="/api")

	return app