from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'fordsEscorts'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Mileage of Ford Escorts'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mileageOnFordsEscorts')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, escorts=result)


@app.route('/view/<int:escort_id>', methods=['GET'])
def record_view(escort_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mileageOnFordsEscorts WHERE id=%s', escort_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', escort=result[0])


@app.route('/edit/<int:escort_id>', methods=['GET'])
def form_edit_get(escort_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mileageOnFordsEscorts WHERE id=%s', escort_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', escort=result[0])


@app.route('/edit/<int:escort_id>', methods=['POST'])
def form_update_post(escort_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('escortYear'), request.form.get('escortMiles'), request.form.get('escortPrice', escort_id))
    sql_update_query = """UPDATE mileageOnFordsEscorts t SET t.escortYear = %s, t.escortMiles = %s, t.escortPrice = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/escorts/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Escort Form')


@app.route('/escorts/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('escortYear'), request.form.get('escortMiles'), request.form.get('escortPrice'))
    sql_insert_query = """INSERT INTO mileageOnFordsEscorts (escortYear,escortMiles,escortPrice) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:escort_id>', methods=['POST'])
def form_delete_post(escort_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mileageOnFordsEscorts WHERE id = %s """
    cursor.execute(sql_delete_query, escort_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/escorts', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mileageOnFordsEscorts')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/escorts/<int:escort_id>', methods=['GET'])
def api_retrieve(escort_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mileageOnFordsEscorts WHERE id=%s', escort_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/escorts/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/escorts/<int:escort_id>', methods=['PUT'])
def api_edit(escort_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/escorts/<int:escort_id>', methods=['DELETE'])
def api_delete(escort_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)