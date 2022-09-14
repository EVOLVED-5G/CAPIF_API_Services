
import os
from flask import Flask
from .controllers.register_controller import register_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)

jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
app.register_blueprint(register_routes)


#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	app.run(debug=True, host = '0.0.0.0', port=8080)
