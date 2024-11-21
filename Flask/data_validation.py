from flask import Flask, jsonify


def validate_no_blanks(new_obj):
    try:
        if new_obj['id']  == '':
            raise ValueError("id missing")
        if new_obj['Title']  == '':
            raise ValueError("title missing")
        if new_obj['Description']  == '':
            raise ValueError("description missing")
        if new_obj['Status']  == '':
            raise ValueError("status missing")
        
        return True

    except ValueError as ex:
        return jsonify(message=str(ex)), 400
    except Exception as ex:
        return jsonify(message=str(ex)), 500
    
def add_to_task_list(new_obj, tasks_list):
    tasks_list.append(new_obj)
    return jsonify(tasks_list), 200


def no_duplicate_id(tasks_list, new_obj):
    for task in tasks_list:
        try:
            if task ['id'] == new_obj['id']:
                raise ValueError("id not available")
            
        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message=str(ex)), 500
    return True


def check_status_content(new_obj):
    allowed_status = ['Complete', 'In Progress', 'To do']
    try:
        if new_obj['Status'] not in allowed_status:
            raise ValueError("Invalid status. Use: To do/In Progress/Complete")
    except ValueError as ex:
            return jsonify(message=str(ex)), 400
    except Exception as ex:
        return jsonify(message=str(ex)), 500
    return True


def verify_id_exists(tasks_list, task_id):
    for task in tasks_list:
        if task['id'] == task_id:
            return task
