from flask import Flask, request, jsonify
import data_validation as dv
import data_management as dm

app = Flask(__name__)
file_path = 'tasks.json'

@app.route("/")
def root():
    print('root of Tasks System')
    return "<h1>Welcome to your Tasks System!</h1>"


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    tasks_list = dm.open_file(file_path)
    if request.method == 'GET':# agregar status para practicar query
        print(len(tasks_list))
        if len(tasks_list) > 0:
            return jsonify (tasks_list)
        else:
            return []
    
    if request.method == 'POST':
        new_id = request.json.get('id')
        new_title = request.json.get('Title')
        new_description = request.json.get('Description')
        new_status =request.json.get('Status')
        new_obj = {'id': new_id, 'Title': new_title,'Description': new_description, 'Status': new_status}
        no_blanks = dv.validate_no_blanks(new_obj)
        no_duplicates = dv.no_duplicate_id(tasks_list, new_obj)
        status_content = dv.check_status_content(new_obj)
        
        if no_blanks != True:
            return no_blanks
        if no_duplicates!= True:
            return no_duplicates
        if status_content!= True:
            return status_content
        else:
            dv.add_to_task_list(new_obj, tasks_list)
            dm.write_file(file_path, tasks_list)
            return jsonify (tasks_list)


@app.route('/tasks/<task_id>', methods=['GET', 'PUT','DELETE'])
def update_tasks(task_id):
    tasks_list = dm.open_file(file_path)
    id_exists = dv.verify_id_exists(tasks_list, task_id)
    if request.method == 'GET':
        if id_exists:
            return jsonify(id_exists), 200
        else:
            return {"msg": "ID not in records!"}, 404

    if request.method == 'PUT':
        for task in tasks_list:
            if task['id'] == task_id:
                updated_id = task_id
                updated_title = request.json.get('Title')
                updated_description = request.json.get('Description')
                updated_status =request.json.get('Status')
                updated_task = {'id': updated_id, 'Title': updated_title,'Description': updated_description, 'Status': updated_status}
                
                no_blanks = dv.validate_no_blanks(updated_task)
                status_content = dv.check_status_content(updated_task)
                
                if no_blanks != True:
                    return no_blanks
                if status_content!= True:
                    return status_content
                
                else:
                    task['id'] = updated_task['id']
                    task['Title'] = updated_task['Title']
                    task['Description'] = updated_task['Description']
                    task['Status'] = updated_task['Status']
                    dm.write_file(file_path, tasks_list)
                    return jsonify(task) 

    if request.method == 'DELETE':
        if id_exists:
            for index, task in enumerate(tasks_list):
                if task['id'] == task_id:
                    tasks_list.pop(index)
                    dm.write_file(file_path, tasks_list)
                    return  jsonify (tasks_list), 200
        else:
            return jsonify(message='ID does not exist'), 404


@app.route('/tasks/filter') #Se activa con localhost/tasks/filter?Status=aqui ponemos es status que queremos filtar (Complete-In Progress-To do).
def filter_by_status():
    dm.open_file(file_path)
    tasks_list = dm.open_file(file_path)
    filtered_tasks = tasks_list
    status_filter = request.args.get('Status')
    if status_filter:
        filtered_tasks = list (
            filter(lambda show: show['Status'] == status_filter, filtered_tasks)
        )
    return {"data": filtered_tasks}


if __name__=="__main__":
    app.run(host="localhost", port=5003, debug=True)