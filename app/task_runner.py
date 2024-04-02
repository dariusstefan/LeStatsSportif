from queue import Queue, Empty
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        self.num_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count())) - 1
        self.task_queue = Queue()
        self.threads = []
        self.graceful_shutdown = Event()
        self.no_more_jobs = False

    def add_task(self, task_id, task):
        if self.no_more_jobs:
            return
        self.task_queue.put((task_id, task))

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
                print("Shutting down thread " + str(self.ident))
                break
            task = self.pool.get_task()
            if task is None:
                continue
            task_id, task = task
            task()


