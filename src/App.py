from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL
import json
import re

app = Flask(__name__)

#Coneccion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pacientesDb'
mysql = MySQL(app)

#Configuraciones
app.secret_key = 'mysecretkey'


#Mostrar pacientes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pacientes')
    data = cur.fetchall()
    return render_template('index.html', patients= data)



#Añadir pacientes
@app.route('/add-patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        palabra = request.form['nombre']
        print(validar_palabra(palabra))
        if validar_palabra(palabra):
            nombre = palabra
        else: nombre = False
        if validar_numero(request.form['peso']):
         peso = float(request.form['peso'])
        else: peso = -1
        if validar_numero(request.form['altura']):
            altura = float(request.form['altura'])
        else: altura = -1      
        if  validar_numero(request.form['grasa']):
            grasa = int(request.form['grasa'])
        else: grasa = -1
        imc = 0
        validarDatos(nombre, peso, altura, grasa, imc)           
    return redirect(url_for('Index'))

#Eliminar pacientes
@app.route("/delete-patient/<string:id>")
def delete_patient(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pacientes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Paciente eliminado correctamente')
    return redirect(url_for('Index'))


def validarDatos(nombre, peso, altura, grasa, imc):
    vNombre = False
    vGrasa = False
    vPeso = False
    vAltura = False

    if not nombre or nombre.count(".") > 0:
        flash('El campo "Nombre" no es valido')
    else: vNombre = True;       
    if  altura < 0 or altura > 3:
        flash('El campo "Altura" no es valido')           
    else: vAltura = True
    if  peso < 0 or peso > 1000:
        flash('El campo "Peso" no es valido')
    else: vPeso = True        
    if grasa < 0 or grasa > 100:
        flash('El campo "% de Grasa" no es valido')
    else: vGrasa = True       
    if vNombre and vAltura and vPeso and vGrasa:
        imc = round(peso/(altura*altura), 2)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pacientes (nombre, peso, altura, grasa, imc) VALUES (%s,%s,%s,%s,%s)",            (nombre, peso, altura, grasa, imc))
        mysql.connection.commit()
        flash('Paciente agregado con exito')

def validar_palabra(palabra):
    patron = '[^0-9_.]+$'
    return bool(re.search(patron, palabra))

def validar_numero(numero):
    patron = '[^a-zA-Z_]'    
    if re.search(patron, numero) and numero.count(".") <= 1:
        return True
    else: return False


if __name__ == '__main__':
    app.run(port=3000, debug=True)





