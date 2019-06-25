from flask import Flask, jsonify, request, make_response
import BaseDatosAgente as db
import random

'''
Variables
'''
# Flask app
app = Flask(__name__)

# Nit of the enterprise
nitG = ''
# Name of the enterprise
empresaG = ''
# Number of the case
casoG = ''
# List of the hostnames of a client
hostNameList = []
# List of service codes of a client
serviceCodeList = []
# Services of a client and their id in th database
serviceDict = dict()
# Name of the service
servicioG = 'default'
# Code of service of the server
serviceCodeG = 'default'
# The service name, hostname or service code the client gives
solicitudG = ''
# Id of the event
eventoG = 0
# name of the user
nombreContG = ''
# Id of the user
cedulaG = 0
# Description of the event
descripcionEventoG = ''
'''
Functions
'''

@app.route('/')
def index():
    return 'Hello World!'

# Gets the JSON of the post method
@app.route('/webhook', methods = ['POST'])
def webhook():

	# Intenta obtener el campo 'action' del json proveninete del post entrante, sino genera un error
	req = request.get_json(force=True)
	try: 
		action = req.get('queryResult').get('action')
	except AttributeError:
		return 'json error'

	# Compares the action from the json to obtain the accurate response

	# Authentication 
	if action == "nit":
		res = 'Super ahora la cedula'
		#res = identifyClient(req['queryResult']['queryText'])

	elif action == "cedula":
		res = 'Genial. Contraseña por favor'
		#res = identifyUser(req['queryResult']['queryText'])

	elif action == "contrasena":
		res = 'y en que te puedo ayudar?'
		#res = validatePassword(req['queryResult']['queryText'])

	# follow-up
	elif action == "casoSeguimiento":
		res = 'Esto fue lo que paso: '
		#res = getLastUpdate(req['queryResult']['queryText'])

	elif action == "contactoEncargado": 
		res = 'regañalo a él'
		#res = getInChargeCase()

	# creation of cases

	elif action == "solicitudCreacionCaso":
		res = 'y sobre que creamos el caso creamos?'
		#res = ciOfClient()

	elif action == "CIafectado":
		res = 'quieres seguir?'
		#res = validarEventosCIafectado(req['queryResult']['queryText'])

	elif action == "CIafectadoNo":
		res = 'gracias'
		#res = CIafectadoNO()

	elif action == "creacionCaso":
		res= 'Se creo el caso'
		#res = creacionCaso(req['queryResult']['queryText'])
	
	# Response to the user
	return make_response(jsonify({'fulfillmentText':res}))

# Identifies the company that is writting through the 'nit' passed by parameter
def identifyClient(req):
	# Guardar el NIT
	cliente = db.identifyClient(req)
	if cliente:
		global nitG
		nitG = cliente[0][0]
		global empresaG
		empresaG = cliente[0][1]
		return 'Ahora por favor, me confirma su numero de cedula'
	else:
		return 'No se encontro una empresa con ese nit'
	# Return Hola empresa con NIT: {}, ahora por favor ingresa tu cedula.format(req)

# Identifies the user through the 'cedula' passed by parameter
def identifyUser(req):
	global cedulaG
	global nombreContG
	global contrasenaG
	contacto = db.identifyUser(req)
	if contacto: 
		if nitG == contacto[0][1]:
			cedulaG = req
			nombreContG = contacto[0][0]
			contrasenaG = contacto[0][2]
			return 'Bienvenido {}, podrias ingresar tu contraseña por favor'.format(nombreContG)
		else:
			return 'No se encontro un cliente con la cedula {} en esa empresa'.format(req)
	# return 'Hola (Nombre de la persona), por favor ingresa tu contraseña'

# Validates that the password of the user is correct and matches the one in the database
def validatePassword(req):
	global nombreContG
	if req == contrasenaG:
		return 'Se ha iniciado sesión como: {}, ¿En qué te puedo colaborar hoy? '.format(nombreContG)
	else:
		return 'contraseña incorrecta'
	# return 'Bienvenido a Claro empresas y negocios. En que puedo colaborarte hoy?'

# Gets the last update of the ongoing case passed by parameter
def getLastUpdate(req):
	global casoG
	casoG = req
	lastUpdate = db.lastUpdate(req)
	# print(lastUpdate)
	# lastUpdate = 'hola'
	return 'La ultima actualización de tu caso es: {}'.format(lastUpdate[0][0])

# get the contact information of the person in charge of the case
def getInChargeCase():
	encargadoDB = db.getInChargeCase(casoG)
	return 'El encargado para el caso {caso} es {encargado} y su extension es: {extension}. En unos segundos comenzará la llamada.'.format(caso = casoG, encargado = encargadoDB[0][0], extension = encargadoDB[0][1])

# Shows all the cis that are linked to the company
def ciOfClient():
	servicesOfClientList = servicesOfClient(nitG)
	string = 'Me podria decir servicio de negocio, codigo de servicio o hostname para el cual necesita la apertura de caso, por favor. Los servicios que se encuentran a nombre de su empresa son: '.format(nombreContG)
	for s in servicesOfClientList:
		string = string + s + ', \n'
	return string

# Checks if there are events for the ci of the client. Asks what the clients will like to do
def validarEventosCIafectado(req):
	global eventoG
	global solicitudG
	global descripcionEventoG
	solicitudG = req
	encontre = False
	ci = servicesOfClient(nitG)
	if req in ci:
		events = db.areThereEvents(nitG)
		for event in events:
			print(event[2])
			if event[2] == req:
				encontre = True
				eventoG = event[0]
				descripcionEventoG = event[1]
				return 'Ya existe un evento en nuestra herramienta de monitoreo para {ciClie} con id {idEvento}, ¿Desea crear un caso de todas maneras?'.format(ciClie = req, idEvento = event[0])
			elif req in event[1]:
				encontre = True
				eventoG = event[0]
				return 'Ya existe un evento en nuestra herramienta de monitoreo para {ciClie} con id {idEvento}, ¿Desea crear un caso de todas maneras?'.format(ciClie = req, idEvento = event[0])
			else:
				continue
		
		if not encontre:
			return 'Me puede describir el problema que se le esta presentando en {}'.format(req)
	else:
		return 'El servicio: {} no se encuentra dentro de la lista de servicios de su empresa'

# Creates follow-up cases
def CIafectadoNO():
	#//TODO
	encontrarValores()
	caso = 'FU' + str(random.randint(1000000, 9999999))
	titulo =  'El cliente se contacto por el evento {}. Se genera caso de seguimiento'.format(eventoG)
	faseActual = 'Registro'
	estado = 'Cerrado'
	grupoAsignacion = 'NULL'
	asignatario = 'NULL'
	categoria = 'NULL'
	subcategoria = 'NULL'
	modelo = 'NULL'
	motivo = 'NULL'
	impacto = 'NULL'
	urgencia = 'NULL'
	prioridad = 'NULL'
	origen = 4
	accionActualizacion = 'NULL'
	db.createCase(caso, titulo, descripcionEventoG, faseActual, estado, cedulaG, nombreContG, empresaG, grupoAsignacion, asignatario, categoria, subcategoria, modelo, motivo, servicioG, serviceCodeG, impacto, urgencia, prioridad, origen, accionActualizacion)
	return 'Se creo el caso de seguimiento {}. Puedo ayudarlo en algo más?'.format(caso)

# Creates the case of the user
def creacionCaso(req):
	#//TODO NombreContacto, companiaNombre, GrupoAsignacion, asignatario, categoria, subcategoria, modelo, motivo, servAfectado, CIAfectado, impacto, urgencia, prioridad, origen, accionActualización
	encontrarValores()
	caso = 'RF' + str(random.randint(1000000, 9999999))
	titulo = 'Requerimiento por parte de {} para el servicio {}'.format(nombreContG, solicitudG)
	faseActual = 'Registro'
	estado = 'Abrir'
	grupoAsignacion = 'NULL'
	asignatario = 'NULL'
	categoria = 'NULL'
	subcategoria = 'NULL'
	modelo = 'NULL'
	motivo = 'NULL'
	impacto = 'NULL'
	urgencia = 'NULL'
	prioridad = 'NULL'
	origen = 4
	accionActualizacion = 'NULL'
	db.createCase(caso, titulo, req, faseActual, estado, cedulaG, nombreContG, empresaG, grupoAsignacion, asignatario, categoria, subcategoria, modelo, motivo, servicioG, serviceCodeG, impacto, urgencia, prioridad, origen, accionActualizacion)
	if servicioG != 'NULL':
		return 'se creo el caso {casoId}, para el cliente: {cliente} ({nit}) con el usuario: {usuario} con cedula: {cc}, para el servicio {servicio} con el motivo de {descripcion}.'.format(casoId = caso, cliente = empresaG, nit = nitG, usuario = nombreContG, cc =cedulaG, servicio = solicitudG, descripcion = req)
	else:
		return 'se creo el caso {casoId}, para el cliente: {cliente} ({nit}) con el usuario: {usuario} con cedula: {cc}, para el servicio {servicio} con el motivo de {descripcion}'.format(casoId = caso, cliente = empresaG, nit = nitG, usuario = nombreContG, cc =cedulaG, servicio = serviceCodeG, descripcion = req)	

# Finds the services that belongs to a client and returns a set of this items
def servicesOfClient(req):
	serviceList = db.findServicesOfClient(nitG)
	global hostNameList
	global serviceCodeList
	global serviceDict
	for tup in serviceList:
		hostNameList.append(tup[0])
		serviceCodeList.append(tup[1])
		serviceDict[tup[2]] = tup[3]
	return set(hostNameList + serviceCodeList + list(serviceDict.values()))

# Finds the values according to the information given by the client
def encontrarValores():
	global servicioG
	global serviceCodeG
	global solicitudG
	if solicitudG in hostNameList:
		serviceCodeG = solicitudG
		serviceG = 'NULL'
	elif solicitudG in serviceCodeList:
		serviceCodeG = db.getHostName(solicitudG)[0][0]
		servicioG = 'NULL'
	else:
		for keyId, val in serviceDict.items():
			if solicitudG == val:
				servicioG = keyId
				serviceCodeG = 'NULL'

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
