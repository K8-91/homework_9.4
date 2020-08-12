from flask import Flask, jsonify
from models import todos
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    artist = request.args.get('artist')
    if artist and len(artist) > 2:
        return jsonify(todos.get_artist(artist))
    return jsonify(todos.all())


@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})


@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json:
        abort(400)
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'artist': request.json.get['artist'],
        'year_of_publication': request.json.get['year_of_publication'],
        'CD_name': request.json.get['CD_name'],
        'my_favourite': request.json.get['my_favourite']
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201


@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def edit_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'artist' in data and not isinstance(data.get('artist'), str),
        'year_of_publication' in data and not isinstance(data.get('year_of_publication'), int),
        'CD_name' in data and not isinstance(data.get('CD_name'), str),
        'my_favourite' in data and not isinstance(data.get('my_favourite'), str)
    ]):
        abort(400)
    todo = {
        'artist': data.get('title', todo['title']),
        'year_of_publication': data.get('year_of_publication', todo['year_of_publication']),
        'CD_name': data.get('CD_name', todo['CD_name']),
        'my_favourite': data.get('my_favourite', todo['my_favourite'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})





if __name__ == "__main__":
    app.run(debug=True)
