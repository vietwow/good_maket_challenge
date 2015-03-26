# This file to wrapper response for this application, we shoudl refactor it soon
from flask import jsonify
import collections

def success(data, list_process=False):
	if list_process:
		result_list = []
		for result in data:
			result_list.append(result._data)
		return jsonify({'status': 'SUCCESS', 'data': result_list})
	else:
		return jsonify({'status': 'SUCCESS', 'data': data})

def error(message, code=400):
    return jsonify({'status': 'ERROR', 'message': message}), code

