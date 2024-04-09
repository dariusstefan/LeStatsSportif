""" This module contains the ThreadPool class and TaskRunner class. """

import os
from queue import Queue, Empty
from threading import Thread, Event

class ThreadPool:
    """ A thread pool that runs tasks in parallel. """
    def __init__(self):
        self.num_threads = int(os.getenv("TP_NUM_OF_THREADS", os.cpu_count())) - 1
        self.task_queue = Queue()
        self.threads = []
        self.jobs = {}
        self.graceful_shutdown = Event()
        self.no_more_jobs = False
        os.makedirs("jobs", exist_ok=True)
        for file in os.listdir("jobs"):
            os.remove(f"jobs/{file}")

    def add_task(self, task_id, task):
        """ Add a task to the task queue. """
        if self.no_more_jobs:
            return
        self.task_queue.put((task_id, task))
        self.jobs[task_id] = "running"

    def get_task(self):
        """ Get a task from the task queue. """
        try:
            return self.task_queue.get(False)
        except Empty:
            if self.no_more_jobs:
                self.graceful_shutdown.set()
            return None

    def init_threads(self):
        """ Initialize the threads in the thread pool. """
        for _ in range(self.num_threads):
            thread = TaskRunner(self)
            self.threads.append(thread)
            thread.start()

    def join_threads(self):
        """ Wait for all threads to finish. """
        for thread in self.threads:
            thread.join()

class TaskRunner(Thread):
    """ A thread that runs tasks."""
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    def run(self):
        """ Run tasks until the pool is shut down. """
        while True:
            if self.pool.graceful_shutdown.is_set():
                break
            task = self.pool.get_task()
            if task is None:
                continue
            task_id, task = task
            output_file = f"jobs/job{task_id}.json"
            with open(output_file, "w", encoding="UTF-8") as file:
                file.write(task())
            self.pool.jobs[task_id] = "done"
