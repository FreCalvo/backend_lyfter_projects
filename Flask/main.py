from flask import Flask, request, jsonify
import data_validation as dv
import data_management as dm
import controller as c
file_path = 'tasks.json'


app = Flask(__name__)

@app.route("/")
def root():
    print('root of Tasks System')
    return "<h1>Welcome to your Tasks System!</h1>"


@app.route('/tasks', methods=['GET', 'POST'])
def show_update_tasks():
    tasks_list = dm.open_file(file_path)
    if request.method == 'GET':
        return c.show_tasks_get(tasks_list)
    
    if request.method == 'POST':
        return c.update_task_post(tasks_list)


@app.route('/tasks/<task_id>', methods=['GET', 'PUT','DELETE'])
def update_tasks(task_id):
    tasks_list = dm.open_file(file_path)
    id_exists = dv.verify_id_exists(tasks_list, task_id)
    if request.method == 'GET':
        return c.update_task_get(id_exists)
    
    if request.method == 'PUT':
        return c.update_task_put(id_exists, task_id, tasks_list)
    
    if request.method == 'DELETE':
        return c.update_task_delete(id_exists, task_id, tasks_list)
    
@app.route('/tasks/filter')
def filter_tasks():
    tasks_list = dm.open_file(file_path)
    return c.filter_by_status(tasks_list)

if __name__=="__main__":
    app.run(host="localhost", port=5003, debug=True)