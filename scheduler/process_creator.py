# modules
from process import Process
from threading import Lock

class ProcessCreator:
    def __init__(self):
        self.__id = 0
        self.__lock = Lock()
        
    def createProcess(self, burst: int) -> Process:
        with self.__lock:
            process = Process(self.__id, None, burst)
            self.__id += 1
            return process
        
    