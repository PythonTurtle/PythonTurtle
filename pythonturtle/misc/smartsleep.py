"""
The Sleeper context manager class implementation.
"""
import time

# from .helpers import log


class Sleeper:
    """
    A smarter way to use `time.sleep()`, implemented as a context manager.
    Use it like this:

    with smartsleep.Sleeper(7):
        do_stuff()

    The Sleeper instance will ensure that at least 7 second have passed before
    control flows to the next lines of code.
    """

    def __init__(self, interval):
        self.interval = interval
        self.starting_time = None

    def __enter__(self, *args, **kwargs):
        self.starting_time = time.time()

    def __exit__(self, *args, **kwargs):
        # global log
        time_now = time.time()
        interval_gone = time_now - self.starting_time
        if interval_gone >= self.interval:
            # log("didn't sleep")
            return
        # log("slept")
        time.sleep(self.interval - interval_gone)
