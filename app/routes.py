from app import webserver
from flask import request, jsonify

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    job_id = int(job_id)
    if webserver.tasks_runner.jobs.get(job_id) is None:
        return jsonify({'status': 'error', 'reason' : 'Invalid job_id'}), 404
    if webserver.tasks_runner.jobs[job_id] == 'running':
        return jsonify({'status': 'running'}), 200
    with open(f"jobs/job{job_id}.json", 'r') as f:
        response = f.read()
        return jsonify({'status': 'done', 'data': json.loads(response)}), 200

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_states_mean_job(request.json['question']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_state_mean_job(request.json['question'], request.json['state']))
    return jsonify({"job_id": webserver.job_counter}), 200


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_best5_job(request.json['question']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_worst5_job(request.json['question']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_global_mean_job(request.json['question']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_diff_from_mean_job(request.json['question']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_state_diff_from_mean_job(request.json['question'], request.json['state']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_mean_by_category_job(request.json['question']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter, webserver.data_ingestor.create_state_mean_by_category_job(request.json['question'], request.json['state']))
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    webserver.tasks_runner.no_more_jobs = True
    webserver.tasks_runner.join_threads()
    return jsonify({"status": "OK"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
