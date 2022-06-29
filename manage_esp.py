from manage_login import *

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

#TAB Pacientes
@app.route('/pacientes_tab')
def pacientes_tab():
    if is_logged():
        #Obtener total de usuarios
        cur = mysql.connection.cursor()
        # Usuario
        cur.execute("SELECT * FROM paciente")
        paciente_list = cur.fetchall()

        cur.close()


        len_paciente_list=len(paciente_list)

        return render_template('pacientes_tab.html', paciente_list= paciente_list, len_paciente_list=len_paciente_list)
    else:
        return redirect(url_for('login'))

# Registro Paciente:
@app.route('/registro_paciente', methods=['GET','POST'])
def registro_paciente():
   
    if request.method == 'POST':
        
        # tabla usuario
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        email = request.form['email']
        numero=  request.form['numero']



        #Para BD sin herencia
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO paciente (nombre, apellido, dni, correo, numero) VALUES (%s,%s,%s,%s,%s)",
            (nombres, apellidos, dni, email, numero))
        mysql.connection.commit()
        cur.close()

        flash('Paciente creado correctamente')
        return redirect(url_for('pacientes_tab'))
    
    return render_template('registro_paciente.html')

#Delete paciente
@app.route('/delete_paciente/<paciente_id>', methods=['GET','POST'])
def delete_paciente(paciente_id):

    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM paciente WHERE id = %s" % (paciente_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('pacientes_tab'))