#Importaciones
from flask import Flask, render_template, request, jsonify
from flask_mysql_connector import MySQL
import webbrowser, os

#Variables Globales
#Variable para app de Flask
aplicacion = Flask(__name__)
#Variable para asignar configuracion de Mysql
mysql = MySQL(aplicacion)
#variable con ruta de la aplicacion
path_actual = os.getcwd()

#Clase para manejo de datos a la base de My SQL
class datas():
    #Configuracion de Base de datos
    aplicacion.config['MYSQL_HOST'] = 'localhost'
    aplicacion.config['MYSQL_USER'] = 'root'
    aplicacion.config['MYSQL_PASSWORD'] = ''
    aplicacion.config['MYSQL_DATABASE'] = 'logyca'
    #Peticion que trae los resultados por numero n
    def objects(n):
        conn = mysql.connection
        cur = conn.cursor()
        sql = f'SELECT * FROM number where number = {str(n)}'
        cur.execute(sql)
        data = cur.fetchone()
        return data
    #Insercion de datos si estos no existen en base de datos numero n, primos y gemelos
    def insert_objects(n,primos,gemelos):
        conn = mysql.connection
        cursor =conn.cursor()
        sql = f'INSERT INTO number (number,primos,gemelos) VALUES ( \'{n}\', \'{primos}\', \'{gemelos}\')'
        cursor.execute(sql)
        conn.commit()
#Clase para funciones con numeros
class numeros():
    #Numeros primos
    def numeros_primos(x):
        #Validador de resultado 1 - es un numero primo
        result = 1
        #iteracion con rango desde 1 hasta un numero menos al que se envia
        
        for i in range(2,x):
            #Cualquier resultado que no cumpla la siguiente coincidencia se toma como un resultado 
            #No primo
            if x % i != 0 and i != 1:
                result = 1
                continue
            else:
                #Si algun valor llega a este punto se detiene iteracion y se asigna 0 a validador
                result = 0
                break
        if result == 1:
            #Si al finalizar todas las iteraciones el resultado continua como 1 se devuelve el numero
            #esto representa que el numero es primo
            return x
        else:
            #Si al finalizar todas las iteraciones o al pasar por el break;
            # se devuelve 0
            #esto representa que el numero no es primo
            return 0

    #Busqueda de gemelos pares de numeros primos 
    #en el cual el segundo valor(mas alto) es el valor uno(mas bajo)+2 
    #[p,p+2]

    #Numeros primos gemelos
    def numeros_gemelos(primos):
        #variable para asignacion de numero primo anterior al que se va a iterar
        anterior = None
        #lista para guardar resultado
        resultados = []
        #iteracion de lista enviada por parametro, con numeros primos 
        for i in primos:
            #si el numero anterior no existe estamos en la primera posicion de la lista
            #esperamos a que haya un valor en esta variable para comparar
            if anterior != None:
                #se compara que restando 2 a el numero en iteracion sea igual al numero anterior 
                if i - 2 == anterior:
                    #se agrega resultado a la lista
                    resultados.append([anterior,i])
            # se asigna valor a variable anterior
            anterior = i
        # se retorna lista con resultados
        return resultados
    #Funcion envio en donde se llaman las funciones de numeros_primos y numeros_gemelos
    def envio(n):
        #se envia comprehension de lista para iterar los valores en un rango de 0 hasta el valor deseado
        #y pasar cada valor por la funcion numeros_primos de la clase numeros
        
        #se obtienen en la variable primos solo los numeros que no devuelvan 0 al pasarlos por la 
        #funcion numeros_primos de la clase numeros
        primos = [item for item in range(0,n+1) if (numeros.numeros_primos(item) != 0)and(item != 1)]
        #variable con resultado obtenido al pasar la lista con numeros primos por la 
        #funcion numeros gemelos de clase numeros
        gemelos = numeros.numeros_gemelos(primos)
        #Si se llega a este punto de calcular las funciones nuemros_primos y numeros_gemelos es 
        #porque no se tenian en la base de datos; entonces se procede a insertar estos valores en esta
        datas.insert_objects(n,primos,gemelos)
        #se retorna lista con resultados
        return [primos,gemelos]
            

    
            

        
            

#Clase para Aplicacion flask
class Aplicacion():
    #Enrutador para inicio de la aplicacion que renderiza el home o index de la aplicacioon
    @aplicacion.route("/")
    #funcion inicio asociada a index
    def inicio():
        #se retorna el template inicio.html para su renderizacion
        return render_template('inicio.html')
    #Enrutador con direccion para hacer peticion get
    @aplicacion.route("/number", methods=['GET'])
    #funcion para devolver la respuetsa de la peticion
    def main():
        #variable para asignar la respuesta de peticion
        respuesta = None
        #se toman los valores enviados
        number = request.args.get('number')
        option = request.args.get('option')
        #se transforman valores a enteros
        number = int(number)
        option= int(option)
        #Se hace peticion a base de datos para consultar si ya existe este nuemro en la base de datos
        dat = datas.objects(number)
        #Condicional para determinar si se devuelve la respuesta de la base de datos
        #En caso de resultar vacia -no se encuentra el numero den base de datos-
        if dat == None:
            #se pasa el numero por las funciones de numeros por medio de funcion envio de clase  numeros
            dat = numeros.envio(number)

            #se asigna la posicion solicitada dependiendo de parametro 
            #opcion 1 primos
            #opcion 2 gemelos
            respuesta = dat[option-1]
        else:
            #se asigna lista directamente desde la respuetsa de la base de datos en caso de que el numero 
            #ya se encuentre en esta
            dat = list(dat)
            #se asigna la posicion solicitada dependiendo de parametro 
            #opcion 1 primos
            #opcion 2 gemelos
            respuesta = dat[option]
        # se parsea la respuesta para su devolucion
        return jsonify(respuesta)
        
        
    
    #creacion de Metodo de principal de aplicacion
    def inicio():
        aplicacion.run()


if __name__ == "__main__":
    #Apertura de Visualizacion de la aplicacion
    webbrowser.open_new('http://127.0.0.1:5000/')
    # llamado a clase de apliocacion y metodo principal de esta
    Aplicacion.inicio()