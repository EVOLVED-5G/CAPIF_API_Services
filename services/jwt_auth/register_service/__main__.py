
import os
from flask import Flask
from .controllers.register_controller import register_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)

jwt = JWTManager(app)

with open("/usr/src/app/register_service/server.key", "rb") as key_file:
            key_data = key_file.read()

app.config['JWT_ALGORITHM'] = 'RS256'
app.config['JWT_PRIVATE_KEY'] = key_data

app.register_blueprint(register_routes)


#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	app.run(debug=True, host = '0.0.0.0', port=8080)
