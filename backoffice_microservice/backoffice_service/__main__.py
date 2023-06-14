from flask import Flask
from .controllers.default_controller import backoffice_routes

app = Flask(__name__)

app.register_blueprint(backoffice_routes)


#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	app.run(debug=True, host = '0.0.0.0', port=8080, ssl_context= ("/usr/src/app/backoffice_service/backoffice_cert.crt", "/usr/src/app/backoffice_service/backoffice_key.key"))
