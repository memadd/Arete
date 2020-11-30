from flask import Flask, jsonify, request

from flask_pymongo import PyMongo

from bson.json_util import dumps 

from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = ("BH54#@aa4lff2")

app.config['MONGO_URI'] = "mongodb://localhost:27017/Students"

mongo = PyMongo(app)


# Create
@app.route('/add', methods=['POST'])
def add_student():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _age = _json['age']
    _grade = _json['grade']
    _number = _json['number']
    _address = _json['address']

    if _name and _email and _age and _grade and _number and _address and request.method == 'POST':
        id = mongo.db.students.insert({"name":_name, "email":_email, "age":_age, "grade":_grade, "number":_number, "address":_address})
        resp = jsonify("Student added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# List
@app.route('/students')
def students():
    students = mongo.db.student.find()
    resp = dumps(students)
    return resp

@app.route('/student/<id>')
def student(id):
    student = mongo.db.student.find_one({'_id':ObjectId(id)})
    resp = dumps(student)
    return resp

# Delete
@app.route('/delete/<id>', methods=['DELETE'])
def delete_student(id):
    mongo.db.student.delete_one({'_id':ObjectId(id)})
    resp = jsonify("Student deleted successfully")

    resp.status_code = 200

    return resp

# Update
@app.route('/update/<id>', methods=['PUT'])
def update_student(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _age = _json['age']
    _grade = _json['grade']
    _number = _json['number']
    _idd = _json['id']
    _address = _json['address']

    if _id and _name and _email and _age and _grade and _number and _idd and _address and request.method == ['PUT']:
        mongo.db.student.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set': {'name':_name, 'email':_email, 'age':_age, 'grade':_grade, 'number':_number, 'id':_idd, 'address':_address}})

        resp = jsonify("Student updated successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()

# Error handler
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404, 
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp 
    

if __name__ == "__main__":
    app.run(debug=True)

