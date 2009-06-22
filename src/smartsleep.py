import time

import sys
def log(text): print(text); sys.stdout.flush()

class Sleeper(object):
    def __init__(self,interval):
        self.interval=interval

    def __enter__(self,*args,**kwargs):
        self.starting_time=time.time()

    def __exit__(self,*args,**kwargs):
        global log
        time_now=time.time()
        interval_gone=time_now-self.starting_time
        if interval_gone>=self.interval:
            #log("didn't sleep")
            return
        else:
            #log("slept")
            time.sleep(self.interval-interval_gone)


