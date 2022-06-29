import datetime
from os import path
#Flask para la app web
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

#Conexión a la BD SQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tdp_5_v2'

#Cursos extraer cosas de la BD
# CURSOR
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Configuracion
app.secret_key = '123456'


# HOME (Página de Inicio)
@app.route('/')
def home():
    return render_template('login.html')

# Comprobar si el usuario esta loggeado
def is_logged():
    if 'usuario' in session:
        return True
    return False

# Logout / Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.clear()
    return redirect(url_for('login'))

#Iniciar sesión
@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']

        if not email or not contrasena:
            error = "Complete los campos necesarios por favor."
        else:    
            cur = mysql.connection.cursor()

            # Usuario
            cur.execute("SELECT * FROM usuario WHERE correo = %s AND idTipo = 1", (email,))
            user = cur.fetchone()
            

            # Psicologo
            cur.execute("SELECT * FROM usuario WHERE correo= %s AND idTipo = 2", (email,))
            escpecialista = cur.fetchone()

            
            cur.close()

            if user is not None and contrasena == user["contrasena"]:
                session["usuario"] = user
                session["nombre"] = user['nombre']
                session["apellido"] = user['apellido']
                session["email"] = user['correo']
                session["contrasena"] = user['contrasena']
                session["dni"] = user['dni']
                return redirect(url_for('user_session'))

            elif escpecialista is not None and contrasena == escpecialista["contrasena"]:
                session["usuario"] = escpecialista
                session["nombre"] = escpecialista['nombre']
                session["apellido"] = escpecialista['apellido']
                session["email"] = escpecialista['correo']
                session["contrasena"] = escpecialista['contrasena']
                session["dni"] = escpecialista['dni']

                return redirect(url_for('esp_session'))
            else:
                error="usuario o contraseña incorrectos. Intentelo de nuevo."

    return render_template('login.html', error=error)



# Registro Alumno:
@app.route('/registro_usuario', methods=['GET','POST'])
def registro_usuario():
   
    if request.method == 'POST':
        
        # tabla usuario
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        email = request.form['email']
        contrasena = request.form['dni']
        estado = request.form['estado']
        tipo = request.form['tipo']


        #Para BD sin herencia
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuario (nombre, apellido, dni, correo, contrasena, idEstadoUsuario, idTipo) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (nombres, apellidos, dni, email, contrasena,estado,tipo))
        mysql.connection.commit()
        cur.close()

        flash('Usuario creado correctamente. Ingrese con su email y contraseña.')
        return redirect(url_for('user_session'))
    
    return render_template('registro_usuario.html')

# Editar Perfil Alumno
@app.route('/editar_perfil_user', methods=['GET','POST'])
def editar_perfil_user():
    if is_logged():

        # ID del alumno
        id_alumno= session['usuario']['id_alumno']
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT * 
            FROM `alumno`
            WHERE id_alumno = %s
            """,
            [id_alumno])
        alumno = cur.fetchone()

        if request.method == 'POST':

            # tabla persona
            nombres = alumno['nombres'] if not request.form['nombres'] else request.form['nombres']
            apellidos = alumno['apellidos'] if not request.form['apellidos'] else request.form['apellidos']
            email = alumno['email'] if not request.form['email'] else request.form['email']
            sede = alumno['sede'] if not request.form['sede'] else request.form['sede']
            contrasena = alumno['contrasena']
            # tabla alumno
            carrera = alumno['carrera'] if not request.form['carrera'] else request.form['carrera']
            sexo = alumno['sexo'] if not request.form['sexo'] else request.form['sexo']
            ciclo = alumno['ciclo'] if not request.form['ciclo'] else request.form['ciclo']
            edad = alumno['edad'] if not request.form['edad'] else request.form['edad']

            #Para BD sin herencia
            # cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE alumno set carrera=%s, edad=%s, ciclo=%s, nombres=%s, apellidos=%s, email=%s, contrasena=%s, sexo=%s, sede=%s WHERE id_alumno=%s",
                (carrera, edad, ciclo, nombres, apellidos, email, contrasena, sexo, sede, id_alumno))
            mysql.connection.commit()
            flash('Cambios guardados correctamente.')

            cur.execute(
                """
                SELECT * 
                FROM `alumno`
                WHERE id_alumno = %s
                """,
                [id_alumno])
            alumno = cur.fetchone()

        cur.close()
        return render_template('editar_perfil_a.html', alumno=alumno)
    else:
        print("No usuario")
        return redirect(url_for('login'))

#Delete user
@app.route('/delete_user/<user_id>', methods=['GET','POST'])
def delete_user(user_id):
    print(user_id)

    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM usuario WHERE id = %s" % (user_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('user_session'))

# Sesión usuario
@app.route('/user_session')
def user_session():
    if is_logged():
        #Obtener total de usuarios
        cur = mysql.connection.cursor()
        # Usuario
        cur.execute("SELECT * FROM usuario")
        users_list = cur.fetchall()
        cur.close()


        len_users_list=len(users_list)

        return render_template('user_session.html', users_list= users_list, len_users_list=len_users_list)
    else:
        return redirect(url_for('login'))

# Sesión especialista
@app.route('/esp_session')
def esp_session():
    if is_logged():
        #Obtener total de usuarios
        cur = mysql.connection.cursor()
        # Usuario
        cur.execute("SELECT * FROM consulta")
        consulta_list = cur.fetchall()
        cur.close()


        len_consulta_list=len(consulta_list)

        return render_template('esp_session.html', consulta_list= consulta_list, len_consulta_list=len_consulta_list)
    else:
        return redirect(url_for('login'))

# MAIN FUNCTION
if __name__ == '__main__':
    app.run(port=3000, debug=True)