'''
	Modules to import
'''
import csv
import mysql.connector

'''
	Variables
'''

'''
Base de datos local
'''
# Name of the database
db_Name = 'claro'
# does the dabase already exists
isCreated = False
# Connection to de DB server
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "Control2019*", buffered = True)
# db manager
mycursor = mydb.cursor()

'''
	functions
'''


'''
	Creates the tables of the database
'''


'''
Finds a client given by the id of the client
'''
def identifyClient(nit):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT * FROM client WHERE nit = \'{}\''.format(nit))
	res = mycursor.fetchall()
	return res

'''
Finds a contact given by the id of the contact
'''
def identifyUser(cedula):
	#cedulaN = int(filter(type(cedula).isdigit, cedula))
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT contactName, clientId, password FROM contact WHERE id = {}'.format(cedula))
	res = mycursor.fetchall()
	return res

'''
Finds a server given by the id of the server
def findServer(codServicio, clientID):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT codServicio FROM servers WHERE hostname = {hostname} and clientId = {clientid}'.format(hostname = codServicio, clientId = clientID))
	res = mycursor.fetchall()
	return res
'''

'''
Finds the servers of a given client
#def findServer(clientID):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT codServicio FROM servers WHERE clientId = {clientid}'.format(clientId = clientID))
	res = mycursor.fetchall()
	return res
'''
'''
Finds a service given by the id of the service
#def findService(id):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT serviceName FROM services WHERE serviceId = {}'.format(id))
	res = mycursor.fetchall()
	return res
'''

'''
Finds a service given by the id of the service
def findServiceName(name):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT * FROM services WHERE serviceName = {}'.format(name))
	res = mycursor.fetchall()
	return res
'''

'''
Finds all the services in a server given by the id of the server
def findServicesInServer(hostName):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT * FROM services WHERE serviceName = {}'.format(name))
	res = mycursor.fetchall()
	return res
'''

'''
def findServersOfClient(clientid):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT * FROM servers WHERE clientId = {}'.format(clientid))
	res = mycursor.fetchall()
	return res
'''

'''
Finds the services of the client given by parameter
'''
def findServicesOfClient(clientid):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT hostname, servers.codServicio, services.serviceId, serviceName FROM services INNER JOIN servicesinserver ON codServicio = codServicio INNER JOIN servers ON servicesinserver.codServicio = servers.codServicio WHERE servers.clientId = \'{}\''.format(clientid))
	res = mycursor.fetchall()
	return res

'''
Creates cases with the info given by parameter
'''
def createCase(numerop, titulop, descripcionp, faseActualp, Estadop, solicitantep, NombreContactop, companiaNombrep, GrupoAsignacionp, asignatariop, categoriap, subcategoriap, modelop, motivop, servAfectadop, CIAfectadop, impactop, urgenciap, prioridadp, origenp, accionActualizacionp):
	mycursor.execute("USE " + db_Name)
	if CIAfectadop != 'NULL':
		mysql = "INSERT INTO cases (numero, titulo, descripcion, faseActual, Estado, solicitante, NombreContacto, companiaNombre, GrupoAsignacion, asignatario, categoria, subcategoria, modelo, motivo, servAfectado, CIAfectado, impacto, urgencia, prioridad, origen, accionActualización) VALUES (\'{numero}\', \'{titulo}\', \'{descripcion}\', \'{faseActual}\', \'{Estado}\', {solicitante}, \'{NombreContacto}\', \'{companiaNombre}\', {GrupoAsignacion}, {asignatario}, {categoria}, {subcategoria}, {modelo}, {motivo}, {servAfectado}, \'{CIAfectado}\', {impacto}, {urgencia}, {prioridad}, {origen}, {accionActualizacion})".format(numero = numerop, titulo = titulop, descripcion = descripcionp, faseActual = faseActualp, Estado = Estadop, solicitante = solicitantep , NombreContacto = NombreContactop, companiaNombre = companiaNombrep, GrupoAsignacion = GrupoAsignacionp, asignatario = asignatariop, categoria = categoriap, subcategoria = subcategoriap, modelo = modelop, motivo = motivop, servAfectado = servAfectadop, CIAfectado = CIAfectadop, impacto = impactop, urgencia = urgenciap, prioridad = prioridadp, origen = origenp, accionActualizacion = accionActualizacionp)
		# print(mysql)
		mycursor.execute(mysql)
	else: 
		mycursor.execute("INSERT INTO cases (numero, titulo, descripcion, faseActual, Estado, solicitante, NombreContacto, companiaNombre, GrupoAsignacion, asignatario, categoria, subcategoria, modelo, motivo, servAfectado, CIAfectado, impacto, urgencia, prioridad, origen, accionActualización) VALUES (\'{numero}\', \'{titulo}\', \'{descripcion}\', \'{faseActual}\', \'{Estado}\', {solicitante}, \'{NombreContacto}\', \'{companiaNombre}\', {GrupoAsignacion}, {asignatario}, {categoria}, {subcategoria}, {modelo}, {motivo}, \'{servAfectado}\', {CIAfectado}, {impacto}, {urgencia}, {prioridad}, {origen}, {accionActualizacion})").format(numero = numerop, titulo = titulop, descripcion = descripcionp, faseActual = faseActualp, Estado = Estadop, solicitante = solicitantep , NombreContacto = NombreContactop, companiaNombre = companiaNombrep, GrupoAsignacion = GrupoAsignacionp, asignatario = asignatariop, categoria = categoriap, subcategoria = subcategoriap, modelo = modelop, motivo = motivop, servAfectado = servAfectadop, CIAfectado = CIAfectadop, impacto = impactop, urgencia = urgenciap, prioridad = prioridadp, origen = origenp, accionActualizacion = accionActualizacionp)
	mydb.commit()

def getHostName(serviceCode):
	mycursor.execute("SELECT hostname FROM servers WHERE codServicio = \'{}\'".format(serviceCode))
	return mycursor.fetchall()


'''
def obtainServiceCod(hostname):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT codServicio from prueba.servers where servers.hostname = \'{}\''.format(hostname))
	res= mycursor.fetchall()
	return res
'''

'''
Finds the code of service from a service.
def findServiceCodeClientService(nitG, servicioG):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT servers.codServicio FROM prueba.services inner join servicesinserver on services.serviceId = servicesinserver.serviceId inner join servers on servicesinserver.codServicio = servers.codServicio where servers.clientId = \'{}\' and services.serviceId = {}'.format(nitG, servicioG))
	res = mycursor.fetchall()
	return res
'''

'''
Find the event with codServicio and nitG given by parameters
'''
def areThereEvents(nitG):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT idEvento, descripcion, codServicio, fecha FROM eventos where cliente = \'{cli}\''.format(cli = nitG))
	mySQL = mycursor.fetchall()
	return mySQL

'''
Gets the person in charge of a client
'''
def getInChargeCase(caso):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT agents.nombre, agents.ext from cases inner join agents on cases.asignatario = agents.id where cases.numero = \'{}\''.format(caso))
	mySQL = mycursor.fetchall()
	return mySQL

'''
Obtains the information of the last update of the case
'''
def lastUpdate(caso):
	mycursor.execute("USE " + db_Name)
	mycursor.execute('SELECT accionActualización from cases where numero = \'{}\''.format(caso))
	mySQL = mycursor.fetchall()
	return mySQL

'''	
main method, creates the database if run as the principal module
'''
if __name__ == "__main__":
	for x in mycursor:
		# print (x)
		if db_Name in x:
			isCreated == True
			break
	if not isCreated:
		CreateDB()
		mycursor.execute("commit")
	else:
		# Indicates what database is going to be used
		mycursor.execute("USE " + db_Name)
		# mycursor.execute("drop schema prueba")
		mycursor.execute("commit")
		CreateDB()