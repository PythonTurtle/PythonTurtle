"""
See documentation for dump_queue defined here.
"""
import Queue


def dump_queue(queue):
    """
    Empties all pending items in a queue
    and returns them in a list.
    """
    result=[]

    while True:
        try:
            thing=queue.get(block=False)
            result.append(thing)
        except Queue.Empty:
            return result

