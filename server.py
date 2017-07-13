from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'secret'
mysql = MySQLConnector(app, 'semirestfulusersdb')

@app.route('/users')
def index():
    query = "SELECT id, CONCAT_WS(' ', first_name, last_name) AS full_name, email, DATE_FORMAT(created_at, '%M %D, %Y') AS created_at FROM users"
    users = mysql.query_db(query)
    return render_template('users.html', users=users)

app.run(debug=True)