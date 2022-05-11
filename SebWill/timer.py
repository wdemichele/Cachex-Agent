import time


class TimerError(Exception):
    """Error in timer usage"""


class Timer:
    """Loosely based on the timer class written by Geir Arne Hjelle in the article
    https://realpython.com/python-timer/"""
    def __init__(self):
        self.count = 0
        self.start_time = None
        self.end_time = None

    def start(self):
        if self.start_time is not None:
            raise TimerError("incorrect use of timer")
        self.start_time = time.perf_counter()

    def stop(self):
        if self.start_time is None:
            raise TimerError("Timer never started, incorrect use of timer")

        time_to_add = time.perf_counter() - self.start_time
        self.start_time = None
        self.count += time_to_add

    def get_count(self):
        return self.count

    def reset_restart(self):
        self.count = 0
        self.start_time = time.perf_counter()

    def reset(self):
        self.count = 0
        self.start_time = None

    def check_time_since_start(self):
        if self.start_time is None:
            raise TimerError("Timer never started, incorrect use of timer")
        time_elapsed = time.perf_counter() - self.start_time
        return time_elapsed
