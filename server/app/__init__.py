from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

# Set up MongoDB
app.config.from_object('config.Config')

mongo = PyMongo(app)

mongo.init_app(app)

# Enable CORS for all routes
CORS(app)

# Register blueprints


def register_blueprints(app):
    from app import views
    app.register_blueprint(views.auth.auth_blueprint)
    app.register_blueprint(views.url.url_blueprint)
    app.register_blueprint(views.analytics.analytics_blueprint)
    app.register_blueprint(views.tag.tag_blueprint)
    app.register_blueprint(views.formerUrl.formerUrl_blueprint)
    app.register_blueprint(views.summary.summary_blueprint)


register_blueprints(app)


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
