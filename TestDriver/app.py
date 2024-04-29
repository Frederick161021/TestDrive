from flask import Flask, render_template, request
from database import Database
from sqlalchemy import text

app = Flask(__name__, static_folder='static')

@app.route('/')
@app.route('/index')
def index():
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
            if not registros:
                print('La consulta no devolvió ningún registro.')
            return render_template('alumnos.html', registros=registros)
        except Exception as e:
            # Maneja el error de alguna manera
            print(e)
            registros = []  # Asigna registros vacíos si hay un error
            return render_template('alumnos.html', registros=registros)
        finally:
            cursor.close()
            connection.close()
        



if __name__ == '__main__':
    app.run(debug=True, port=5000)
