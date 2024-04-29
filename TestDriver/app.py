from flask import Flask, render_template, request
from database import Database

app = Flask(__name__, static_folder='static')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/registroAlumnos', methods=['GET', 'POST'])
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
        
        db = Database.getInstance()
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
