""" This module contains the routes for the webserver. """

import json
from flask import request, jsonify
from app import webserver

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """ Returns the status of all the jobs. """
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    return jsonify({'status': 'done', 'jobs': webserver.tasks_runner.jobs}), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    """ Returns the number of running jobs. """
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    num_jobs = len([x for x in webserver.tasks_runner.jobs.items() if x[1] == 'running'])
    return jsonify({'status': 'done', 'num_jobs': num_jobs}), 200

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """ Returns the results of the job with the given job_id. """
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    job_id = int(job_id)
    if job_id not in webserver.tasks_runner.jobs:
        webserver.logger.info("Invalid job_id: %d.", job_id)
        return jsonify({'status': 'error', 'reason' : 'Invalid job_id'}), 404
    if webserver.tasks_runner.jobs[job_id] == 'running':
        return jsonify({'status': 'running'}), 200
    with open(f"jobs/job{job_id}.json", "r", encoding="UTF-8") as file:
        response = file.read()
        return jsonify({'status': 'done', 'data': json.loads(response)}), 200

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """ Handles the request for the states mean."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_states_mean_job(request.json['question']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """ Handles the request for the state mean."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_state_mean_job(request.json['question'],
                                                              request.json['state']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """ Handles the request for the best5."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_best5_job(request.json['question']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """ Handles the request for the worst5."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_worst5_job(request.json['question']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """ Handles the request for the global mean."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_global_mean_job(request.json['question']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """ Handles the request for the diff_from_mean."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_diff_from_mean_job(request.json['question']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """ Handles the request for the state_diff_from_mean."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_state_diff_from_mean_job(request.json['question'],
                                                                        request.json['state']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """ Handles the request for the mean_by_category."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_mean_by_category_job(request.json['question']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """ Handles the request for the state_mean_by_category."""
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    if webserver.tasks_runner.no_more_jobs:
        webserver.logger.info("Threads are shutdown. No more jobs accepted.")
        return jsonify({'status': 'error', 'reason' : 'No more jobs allowed'}), 503
    webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.job_counter,
                webserver.data_ingestor.create_state_mean_by_category_job(request.json['question'],
                                                                          request.json['state']))
    webserver.logger.info("Server allocated job_id: %d.", webserver.job_counter)
    return jsonify({"job_id": webserver.job_counter}), 200

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """ Gracefully shuts down the webserver. """
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    webserver.logger.info("Shutting down the threads. No more jobs will be accepted.")
    webserver.tasks_runner.no_more_jobs = True
    webserver.tasks_runner.join_threads()
    return jsonify({"status": "OK"}), 200

@webserver.route('/')
@webserver.route('/index')
def index():
    """ Returns the index page of the webserver. """
    webserver.logger.info("Received request '%s %s %s' from %s.",
                                    request.method,
                                    request.path,
                                    request.environ.get('SERVER_PROTOCOL'),
                                    request.remote_addr)
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """ Returns the defined routes of the webserver. """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
