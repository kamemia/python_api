from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)

database_name = "API"
DB_URI = "mongodb+srv://kamemia:Oto6XLsxvG56t3iV@cluster0.fsk7brs.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


class Record(db.Document):
    record_id = db.IntField()
    first_name = db.StringField()
    last_name = db.StringField()
    age = db.IntField()

    def to_json(self):
        # Converts the document to json
        return {
            "record_id": self.record_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age
        }


@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    pass


@app.route('/api/records', methods=['GET', 'POST'])
def api_records(records=None):
    if request.method == 'GET':
        print(request.method)
        record = []
        for record in Record.objects:
            records.append(record)
        return make_response(jsonify(records), 200)
    elif request.method == 'POST':
        content = request.json
        record = Record(record_id=content['record_id'],
                        first_name=content['first_name'], last_name=content['last_name'],
                        age=content['age'])
        record.save()
        return make_response("", 201)


@app.route('/api/records/<records_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_record(record_id):
    if request.method == 'GET':
        record_obj = Record.objects(record_id=record_id).first()
        if record_obj:
            return make_response(jsonify(record_obj.to_json()), 200)
        else:
            return make_response("", 404)
    elif request.method == 'PUT':
        content = request.json
        record_obj = Record.objects(record_id=record_id).first()
        record_obj.update(first_name=content['first_name'], last_name=content['last_name'], age=content['age'])
        return make_response("", 204)

    elif request.method == "DELETE":
        record_obj = Record.objects(record_id=record_id).first()
        record_obj.delete()
        return make_response("", )
    pass


if __name__ == '__main__':
    app.run()
