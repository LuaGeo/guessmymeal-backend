from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app.routes.food_routes import food_bp
app.register_blueprint(food_bp, url_prefix='/api')