'''
Libraries and frameworks
'''
from flask import Flask, jsonify, request, make_response, Response
import BaseDatosAgente as db
import logging
from functools import wraps

'''
Creates an instance of the flask class
'''
app = Flask(__name__)

'''
functions
'''

'''
Authentication and authorization methods
'''

'''
Gives or denies the authorization
'''
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwards):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwards)
	return decorated
'''
Checks that the information provided by the user matches the information on the database
'''
def check_auth(username, password):
	uname = "myuser"
	pwd = "mypassword"
	return username == uname and password == pwd

'''
sends an error message if the logging information is incorrect
'''
def authenticate():
	return Response('Invalid login, \n'
		'Invalid login.', 401,
		{'www-Authenticate' : 'Basic realm="Login Required"'})

'''
Conversation functions
'''

'''
Function that handles the conversation with the 'action' parameter
'''
@app.route('/', methods=['POST'])
#@requires_auth
def handle():
	# Intenta obtener el campo 'action' del json proveninete del post entrante, sino genera un error
	req = request.get_json(force=True)
	print(req)
	try: 
		action = req.get('queryResult').get('action')
	except AttributeError:
		return 'json error'

	# Compares the action from the json to obtain the accurate response
	if action == "cedula":
		res = 'Por favor ingresa tu contraseña'
	elif action == "contrasena":
		res = 'Bienvenido @name, en que te podemos ayudar el día de hoy?'
	elif action == "seguimiento":
		res = 'tienes el número del caso?'
		#res = getLastUpdate(req)
	elif action == "identificador":
		res = 'La ultima actualización de tu caso es:'
	elif action == "seguimientoNotOkYes":
		res = 'esto no esta bien, llama al encargado henry'
	elif action == "seguimientoNotOk-no-no":
		res = 'Henry! crea un caso de seguimiento YA!'
	elif action == 'requerimiento':
		res = 'Vamos a crear un requerimiento'
	elif action == 'incidente':
		res = 'Vamos a crear un incidente'
	

	# Response for the user
	return make_response(jsonify({'fulfillmentText':res}))



if __name__ == "__main__":
	app.run(debug = True)