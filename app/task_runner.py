from queue import Queue, Empty
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        self.num_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count())) - 1
        self.task_queue = Queue()
        self.threads = []
        self.jobs = {}
        self.graceful_shutdown = Event()
        self.no_more_jobs = False
        os.makedirs("jobs", exist_ok=True)
        for file in os.listdir("jobs"):
            os.remove(f"jobs/{file}")

    def add_task(self, task_id, task):
        if self.no_more_jobs:
            return
        self.task_queue.put((task_id, task))
        self.jobs[task_id] = 'running'

    def get_task(self):
        try:
            return self.task_queue.get(False)
        except Empty:
            if self.no_more_jobs:
                self.graceful_shutdown.set()
            return None

    def init_threads(self):
        for i in range(self.num_threads):
            thread = TaskRunner(self)
            self.threads.append(thread)
            thread.start()
    
    def join_threads(self):
        for thread in self.threads:
            thread.join()

class TaskRunner(Thread):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    def run(self):
        while True:
            if self.pool.graceful_shutdown.is_set():
                break
            task = self.pool.get_task()
            if task is None:
                continue
            task_id, task = task
            output_file = f"jobs/job{task_id}.json"
            with open(output_file, "w") as f:
                f.write(task())
            self.pool.jobs[task_id] = 'done'
