import threading
from queue import Queue
import concurrent.futures


class FunctionalProcessor:
    def __init__(self, num_threads=5, timeout=None):
        self.num_threads = num_threads
        self.queue = Queue()
        self.results = {}
        self.lock = threading.Lock()
        self.threads = []
        self.task_counter = 0  # Ensure unique task IDs
        self.timeout = timeout  # Timeout for each task

    def worker(self):
        while True:
            function, args, kwargs, task_id = self.queue.get()
            if function is None:
                break
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(function, *args, **kwargs)
                    result = future.result(timeout=self.timeout)
            except concurrent.futures.TimeoutError:
                result = f"Task {task_id} timed out."
            except Exception as e:
                result = f"Task {task_id} failed with exception: {str(e)}"
            with self.lock:
                self.results[task_id] = result
            self.queue.task_done()

    def add_task(self, function, *args, **kwargs):
        with self.lock:
            task_id = self.task_counter
            self.task_counter += 1
        self.queue.put((function, args, kwargs, task_id))
        return task_id

    def start_threads(self):
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_threads(self):
        for _ in self.threads:
            self.queue.put((None, None, None, None))

        for thread in self.threads:
            thread.join()

    def get_result(self, task_id):
        return self.results.get(task_id)

    def wait_for_completion(self):
        self.queue.join()  # Wait for all tasks to be processed


# Example usage
'''
import time


# Sample function to process
def sample_function(x, y):
    time.sleep(1)  # Simulate some delay
    return x + y


# Create instance of the processor
processor = FunctionProcessor(num_threads=3)

# Start worker threads
processor.start_threads()

# Add tasks to the queue
task1 = processor.add_task(sample_function, 1, 2)
task2 = processor.add_task(sample_function, 10, 20)
task3 = processor.add_task(sample_function, 100, 200)

# Wait for tasks to finish
processor.wait_for_completion()

# Fetch results
print("Task 1 result:", processor.get_result(task1))  # Output: 3
print("Task 2 result:", processor.get_result(task2))  # Output: 30
print("Task 3 result:", processor.get_result(task3))  # Output: 300

# Stop threads after completion
processor.stop_threads()'''
