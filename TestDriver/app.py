from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
import random
import datetime

app = Flask(__name__, static_folder='static')

app.secret_key = 'tu_clave_secreta_aqui'


@app.route('/')
@app.route('/index')
def index():
    session['index'] = 0
    session['puntos'] = 0.0
    return render_template('index.html')

@app.route('/registroAlumnos', methods=['POST', 'GET'])
def registroAlumnos():
    context={
        "type": "",
        "mensaje": ""
    }

    if request.method == 'POST':
        matricula = request.form['matricula']
        nombre = request.form['nombre']
        apellido_paterno = request.form['paterno']
        apellido_materno = request.form['materno']
        email = request.form['email']
        telefono = request.form['telefono']
        
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        try:
            cursor.callproc('agregarEstudiante', (matricula, nombre, apellido_paterno, apellido_materno, email, telefono))
            connection.commit()
            context["type"] = "success"
            context["mensaje"] = "Estudiante agregado correctamente!"
        except Exception as e:
            # connection.rollback()
            context["type"] = "danger"
            context["mensaje"]= "Error al agregar estudiante"
        finally:
            cursor.close()
            connection.close()
            return render_template('registroAlumnos.html', context=context)
    else:
        return render_template('registroAlumnos.html', context=context)



@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'GET':
        registros = []
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute('CALL consultarEstudiante()')

        registros = cursor.fetchall()
        # print(registros[0])

        cursor.close()
        connection.close()

        return render_template('alumnos.html', registros = registros)
        
    elif request.method == 'POST':
        matricula = request.form['matricula']

        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('CALL consultarPorMatriculaEstudiante(%s)', [matricula])
            registros = cursor.fetchall()
            return render_template('alumnos.html', registros=registros)
        except Exception as e:
            # Maneja el error de alguna manera
            print(e)
            registros = []  # Asigna registros vacíos si hay un error
            return render_template('alumnos.html', registros=registros)
        finally:
            cursor.close()
            connection.close()
        

@app.route('/presentarExamen', methods=['GET', 'POST'])
def presentarExamen():
    mensaje = ""
    if request.method == 'POST':
        matricula = request.form['matricula']

        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('CALL contarExamenes(%s)', [matricula])
            numeroPruebas = cursor.fetchall()[0][0]
            if numeroPruebas <= 3 :
                context = {'matricula': matricula, 'preguntasId': seleccionPreguntasExamen(40), 'index':0, 'numPreguntas': 40, 'puntos':0.0}
                return redirect(url_for('examen', **context))
            else:
                mensaje = "Ya no puedes presentar más examenes!"
                return render_template('indentificacion.html', mensaje = mensaje) 
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    return render_template('identificacion.html', mensaje = mensaje)


@app.route('/presentarExamenPrueba', methods=['GET', 'POST'])
def presentarExamenPrueba():
    mensaje = ""
    if request.method == 'POST':
        matricula = request.form['matricula']

        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('CALL contarPruebaManejo(%s)', [matricula])
            numeroPruebas = cursor.fetchall()[0][0]
            if numeroPruebas <= 6 :
                preguntasId = seleccionPreguntasExamen(20)
                context = {'matricula': matricula, 'preguntasId': preguntasId, 'index':0, 'numPreguntas': 20, 'puntos':0.0}
                return redirect(url_for('examen', **context))
            else:
                mensaje = "Ya no puedes presentar más examenes de prueba!"
                return render_template('identificacion.html', mensaje = mensaje)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    return render_template('identificacion.html', mensaje = mensaje)



@app.route('/examen', methods=['GET', 'POST'])
def examen():
    matricula = request.args.get('matricula')
    preguntasId = request.args.getlist('preguntasId')
    index = session.get('index', 0)  # Obtener el índice de la sesión, con un valor predeterminado de 0
    numPreguntas = int(request.args.get('numPreguntas'))
    puntos = session.get('puntos', 0.0)   # Obtener los puntos de la sesión, con un valor predeterminado de 0

    registros = []

    if request.method == 'GET':
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        
        preguntaId = int(preguntasId[index])
        
        cursor.execute('CALL obtenerDatosPregunta(%s)', [preguntaId])
        registros = cursor.fetchall()

        cursor.close()
        connection.close()

        context = {'matricula': matricula, 'preguntasId': preguntasId, 'index': index+1, 'numPreguntas': numPreguntas, 'puntos': puntos}

        return render_template('examen.html', registros = registros, context = context)


    if request.method == 'POST':
        try:
            opcion_seleccionada = int(request.form['opcion'])
            print("opcion seleccionada: %s" % opcion_seleccionada)
            if opcion_seleccionada == 1 :
                print(numPreguntas)
                if numPreguntas == 20 :
                    print ("prueba")
                    puntos += 5
                    session['puntos'] = puntos
                    print('puntos %d' % puntos)
                elif numPreguntas == 40 :
                    puntos += 2.5
                    session['puntos'] = puntos
                    print('puntos %d' % float(puntos))

        except KeyError:
            print("Ninguna opción seleccionada.")

        index += 1  # Incrementar el índice
        session['index'] = index  # Actualizar el índice en la sesión

        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        
        preguntaId = int(preguntasId[index])
        
        cursor.execute('CALL obtenerDatosPregunta(%s)', [preguntaId])
        registros = cursor.fetchall()

        context = {'matricula': matricula, 'preguntasId': preguntasId, 'index': index, 'numPreguntas': numPreguntas, 'puntos': puntos}
        
        
        cursor.close()
        connection.close()

        if index ==  len(preguntasId)-1:
            fecha = datetime.date.today()
            tipo = ""
            resultados ={'mensaje': "", 'imagen': ""}


            if numPreguntas == 20:
                calificacion = ((puntos / 5) * 100) / numPreguntas
                tipo = "Test"
            elif numPreguntas == 40:
                calificacion = ((puntos / 2.5) * 100) / numPreguntas
                tipo = "Final"



            if calificacion >= 75 :
                resultados['mensaje'] = "Aprobaste el examen con: %s , Felicidades!" %calificacion
                resultados['imagen'] = "../static/img/aprobado.jpg"
            elif calificacion < 75:
                resultados['mensaje'] = "Reprobaste con %s, suerte para la proxima!" %calificacion
                resultados['imagen'] = "../static/img/reprobado.png"
            
            db = Database()
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('CALL registrarExamenHistorial(%s, %s, %s, %s)', (matricula, fecha, tipo, calificacion))
            connection.commit()

            cursor.close()
            connection.close()
            return redirect(url_for('resultado', **resultados))
        else:
            return render_template('examen.html', registros = registros, context = context)



def seleccionPreguntasExamen(numeroPreguntas):
    numeros = random.sample(range(1, 101), numeroPreguntas)
    return numeros


@app.route('/resultado', methods = ['POST', 'GET'])
def resultado():
    mensaje = request.args.get('mensaje')
    imagen = request.args.get('imagen')
    resultados = {'mensaje':mensaje, 'imagen':imagen}
    print (resultados)
    return render_template('resultado.html', resultados = resultados)



@app.route('/historial', methods = ['POST', 'GET'])
def historial():
    if request.method == 'GET':
        registros = []
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute('CALL consultarHistorial()')

        registros = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('historial.html', registros = registros)


if __name__ == '__main__':
    app.run(debug=True, port=5000)