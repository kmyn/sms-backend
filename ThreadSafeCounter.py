import threading


class ThreadSafeCounter():
    def __init__(self):
        self.lock = threading.Lock()
        self.counter = 0

    def increment(self):
        with self.lock:
            self.counter += 1

    def incrementBy(self, val):
        with self.lock:
            self.counter += val

    def decrement(self):
        with self.lock:
            self.counter -= 1

    def reset(self):
        with self.lock:
            self.counter = 0

    def get(self):
        return self.counter
