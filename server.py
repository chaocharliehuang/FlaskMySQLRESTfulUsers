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

@app.route('/users/<id>')
def show(id):
    data = {'id': int(id)}
    query = "SELECT id, CONCAT_WS(' ', first_name, last_name) AS full_name, email, DATE_FORMAT(created_at, '%M %D, %Y') AS created_at FROM users WHERE id = :id LIMIT 1"
    user = mysql.query_db(query, data)
    return render_template('show.html', user=user[0])

@app.route('/users/<id>', methods=['POST'])
def update(id):
    update_data = {
        'id': int(id),
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
        }
    update_query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
    mysql.query_db(update_query, update_data)
    return redirect('/users/' + id)

@app.route('/users/<id>/edit')
def edit(id):
    data = {'id': int(id)}
    query = "SELECT id, first_name, last_name, email FROM users WHERE id = :id LIMIT 1"
    user = mysql.query_db(query, data)
    return render_template('edit.html', user=user[0])

@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/create', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']

    # FORM VALIDATION
    if len(first_name) < 2 or len(last_name) < 2 or not first_name.isalpha() or not last_name.isalpha():
        flash('First and last names must be at least 2 characters and only contain letters!')
        return redirect('/users/new')

    if len(email) < 1:
        flash('Email cannot be blank!')
        return redirect('/users/new')
    elif not EMAIL_REGEX.match(email):
        flash('Invalid email address!')
        return redirect('/users/new')

    # INSERT NEW USER INTO DATABASE
    insert_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }
    insert_query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    new_user_id = mysql.query_db(insert_query, insert_data)

    return redirect('/users/' + str(new_user_id))

@app.route('/users/<id>/destroy', methods=['POST'])
def destroy(id):
    delete_data = {'id': int(id)}
    delete_query = "DELETE FROM users WHERE id = :id"
    mysql.query_db(delete_query, delete_data)
    return redirect('/users')

app.run(debug=True)