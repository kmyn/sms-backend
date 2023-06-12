import threading
from queue import Queue
from ThreadSafeCounter import ThreadSafeCounter

queue = Queue()

# Lock to protect only one simulation from running
simulationInitLock = threading.Lock()

# Sender stats. As multiple threads are accessing the stats, counters need to
# be thread safe.
senderStats = {
    "received": ThreadSafeCounter(),
    "processed": ThreadSafeCounter(),
    "errors": ThreadSafeCounter(),
    "processingTime": ThreadSafeCounter()
}

# Number of active senders
activeSenders = ThreadSafeCounter()

# Get number of messages (requests) in queue to be processed
def getQueueSize():
    return queue.qsize()


# Get sender stats
def getSenderStats():
    stats = {}
    for key in senderStats:
        if key == 'processingTime':
            stats['avgProcessingTime'] = round(senderStats[key].get()/senderStats["processed"].get(), 2) if senderStats[key].get() else 0
        else:
            stats[key] = senderStats[key].get()
    return stats

# Reset sender simulation stats
def resetSimulation():
    queue.queue.clear()
    for key in senderStats:
        senderStats[key].reset()
    activeSenders.reset()

# Number of active senders
def getActiveSenders():
    return activeSenders.get()

# Returns boolean to indicate if simulation is actively running or not
def isSimulationRunning():
    return (getActiveSenders() != 0)
