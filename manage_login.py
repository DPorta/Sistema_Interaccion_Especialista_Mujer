from config import *

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
