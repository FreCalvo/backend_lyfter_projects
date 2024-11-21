from flask import request, jsonify
import data_validation as dv
import data_management as dm

file_path = 'tasks.json'

def show_tasks_get(tasks_list):
    if len(tasks_list) > 0:
            return jsonify (tasks_list)
    else:
        return []


def update_task_post(tasks_list):
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


def update_task_get(id_exists):
    if id_exists:
        return jsonify(id_exists), 200
    else:
        return {"msg": "ID not in records!"}, 404


def update_task_put(id_exists, task_id, tasks_list):
    if id_exists:
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
    else:
        return jsonify(message='ID does not exist'), 404


def update_task_delete(id_exists, task_id, tasks_list):
    if id_exists:
        for index, task in enumerate(tasks_list):
            if task['id'] == task_id:
                tasks_list.pop(index)
                dm.write_file(file_path, tasks_list)
                return  jsonify (tasks_list), 200
    else:
        return jsonify(message='ID does not exist'), 404


def filter_by_status(tasks_list):
    # dm.open_file(file_path)
    # tasks_list = dm.open_file(file_path)
    filtered_tasks = tasks_list
    status_filter = request.args.get('Status')
    if status_filter:
        filtered_tasks = list (
            filter(lambda show: show['Status'] == status_filter, filtered_tasks)
        )
    return {"data": filtered_tasks}