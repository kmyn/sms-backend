import string
import numpy as np
from threading import Thread

from globals import queue

# Producer
# Sends messages in the form of {message: "xxxxx", phone: "2323232"} to the queue.
class Producer(Thread):

    def __init__(self, numMessages):
        Thread.__init__(self)
        self.numMessages = numMessages
        self.messagesSent = 0

    def getMessage(self):
        return ''.join(np.random.choice(list(string.ascii_lowercase),  size=(100)))

    def getPhoneNumber(self):
        phoneNumber = np.random.randint(9, size=(10))
        return ''.join(map(str, phoneNumber))

    def run(self):
        # create thread pool
        for i in range(self.numMessages):
            value = {
                "message": self.getMessage(),
                "phone": self.getPhoneNumber()
            }

            # push data into queue
            queue.put(value)
            self.messagesSent += 1

        print('Producer sent: ', self.messagesSent)
