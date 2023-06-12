import random
import queue as Queue
from threading import Thread
from time import sleep

from globals import queue, senderStats, activeSenders

# Sender
# Dequeues messages from the queue (put by the producer) and simulates a job.
class Sender(Thread):

    def __init__(self, failureRate):
        Thread.__init__(self)
        self.failureRate = failureRate

    def run(self):
        activeSenders.increment()

        while True:
            try:
                # Wait 'timeout' seconds to dequeue and if
                # unable to dequeue implies there are no
                # messages in queue
                message = queue.get(timeout=2)
                senderStats["received"].increment()

                # Skip message based on failure rate
                if random.random() < self.failureRate:
                    senderStats["errors"].increment()
                    continue

                senderStats["processed"].increment()

                # Mimic operate on 'message' by sleep between 0 ~ 5sec
                processTime = random.randint(0, 5)
                sleep(processTime)

                senderStats["processingTime"].incrementBy(processTime)
            except Queue.Empty:
                break

        # Once thread is complete, decrement active sender
        activeSenders.decrement()
