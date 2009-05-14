import multiprocessing

class Reporter(object):
    """
    improve it so there's always an available report
    """

    def __init__(self):
        self.queue=multiprocessing.Queue(maxsize=1)

    def send_report(self,report):
        self.queue.get(block=False)
        self.queue.put(report)

    def get_report(self,block=True):
        return self.queue.get(block)