import re
from manage_login import *
# Registro Usuario:
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
@app.route('/edit_user/<user_id>', methods=['GET','POST'])
def edit_user(user_id):
    if is_logged():
        cur = mysql.connection.cursor()
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
                cur.execute(
                    "UPDATE usuario set nombre=%s, apellido=%s, dni=%s, correo=%s, contrasena=%s, idEstadoUsuario=%s, idTipo=%s WHERE id=%s",
                    (nombres, apellidos, dni, email, contrasena, estado, tipo, user_id))
                mysql.connection.commit()
                return redirect(url_for('user_session'))
        
        cur.execute(
            """
            SELECT * 
            FROM `usuario`
            WHERE id = %s
            """,
            [user_id])
        user = cur.fetchone()
        cur.close()

        return render_template('edit_user.html', user=user)
    else:
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