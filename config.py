#Flask para la app web
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from manage_user import *

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