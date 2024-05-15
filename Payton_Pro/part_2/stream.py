import threading
from typing import Callable

class Stream:
    def __init__(self) -> None:
        self.list = []
        self.task = None
        self.next_processor = None
        self.flagToStop = False
        self.condition = threading.Condition()
        self.thread1 = threading.Thread(target=self.worker, daemon=False)
        self.childTreads = []
        self.thread1.start()

    def add(self, x):
        with self.condition:
            self.list.append(x)
            self.condition.notify()

    def worker(self):        
        while True:
            with self.condition:
                while not self.flagToStop and not self.list:
                    self.condition.wait()
                if self.flagToStop:
                    break
                if self.list and self.task:
                    item = self.list.pop(0)
                    if item is not None:                    
                        result = self.task(item)
                        if result is not None and self.next_processor is not None:
                            if isinstance(result, bool):
                                if result:
                                    self.next_processor.add(result)
                            else:
                                self.next_processor.add(result)

    def forEach(self, func):
        self.task = func
        self.next_processor = None
        with self.condition:
            self.condition.notify()

    def apply(self, func):      
        newStream = Stream()
        self.next_processor = newStream
        self.childTreads.append(newStream)

        def applyAction(x):
            result = func(x)
            if isinstance(result, bool):
                if result:
                    newStream.add(x)
            elif isinstance(result, int):
                newStream.add(result)

        self.forEach(applyAction)
        return newStream

    def stop(self):
        with self.condition:
            self.flagToStop = True
            self.condition.notify_all()
        self.thread1.join()

        for x in self.childTreads:
            x.stop()

        if self.next_processor:
            self.next_processor.stop()

        with self.condition:
            self.list.clear()
            
        self.next_processor = None
