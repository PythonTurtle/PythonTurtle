from shell import Shell
from console import Console
import multiprocessing

def make_queue_pack():
    return [multiprocessing.Queue() for i in range(4)]

__all__=["Shell","Console","make_queue_pack"]