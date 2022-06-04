from email import message
import json
from urllib import response
from wsgiref.util import request_uri
from xmlrpc.client import ResponseError
import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


@app.route('/create', methods=['POST'])
def create_user():
    try:
        _json = request.json
        _fname = _json['fname']
        _lname = _json['lname']
        _age = _json['age']
        _id = _json['id']
        if _fname and _lname and _age and _id and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO user(fname, lname, age, id) VALUES(%s, %s, %s, %s)"
            bindData = (_fname, _lname, _age, _id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('User added successfully')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user')
def user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT fname, lname, age, id FROM user')
        userRows = cursor.fetchall()
        response = jsonify(userRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found:' + request_uri,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run()
