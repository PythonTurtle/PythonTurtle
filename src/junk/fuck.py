import time
import sys
from multiprocessing import *

class MyProcess(Process):
    def run(self):
        self.x=["ooga","booga"]
        print("did it"); sys.stdout.flush()
        q=Queue()
        q.get()

if __name__=="__main__":
    p=MyProcess()
    print(p.is_alive())
    p.start()
    
    print(p.is_alive())
    time.sleep(5)
    print(p.is_alive())
    print(p.x)
    
