""" This module initializes the webserver and sets up the logger, 
the thread pool and the data ingestor. """

import logging
import logging.handlers
import time
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.json.sort_keys = False

webserver.logger = logging.getLogger(__name__)
webserver.logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler("webserver.log", maxBytes=4000, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d/%m/%Y %H:%M:%S")
formatter.converter = time.gmtime
handler.setFormatter(formatter)

webserver.logger.addHandler(handler)

webserver.logger.info("Webserver started")

webserver.tasks_runner = ThreadPool()

webserver.tasks_runner.init_threads()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 0

from app import routes
