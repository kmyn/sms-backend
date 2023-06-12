from flask import Flask, request, jsonify
from flask_cors import CORS

from Sender import Sender
from Producer import Producer
from globals import simulationInitLock, resetSimulation, getSenderStats, isSimulationRunning
from utils import is_float


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/', methods=['GET'])
    def index():
        return 'SMS Simulation App'

    # Route to get simulation status
    @app.route('/sim/status', methods=['GET'])
    def simulation_status():

        # If there is no active simulation then, we return
        # the stats of the last run simulation
        resp = jsonify({
            'status': 'SUCCESS',
            'isActive': isSimulationRunning(),
            'stats': getSenderStats()
        })
        resp.status_code = 200
        return resp

    # Route to start simulation
    @app.route('/sim/start', methods=['POST'])
    def simulation_start():
        # Acquire lock to avoid race condition where 2 clients
        # are trying to start simulation
        simulationInitLock.acquire()

        # Only one simulation can be active at a time
        if isSimulationRunning():
            resp = jsonify({
                'status': 'CONFLICT'
            })
            resp.status_code = 200
            simulationInitLock.release()
            return resp

        requestData = request.get_json()

        numMessages = 1000
        failureRate = None
        numSenders = None

        if requestData:
            if 'numMessages' in requestData:
                if str(requestData['numMessages']).isnumeric():
                    numMessages = int(requestData['numMessages'])
                else:
                    numMessages = None

            if 'failurePct' in requestData and (str(requestData['failurePct']).isnumeric() or is_float(requestData['failurePct'])):
                failurePct = int(requestData['failurePct']) if str(requestData['failurePct']).isnumeric() else float(requestData['failurePct'])
                failureRate = failurePct / 100

            if 'numSenders' in requestData and str(requestData['numSenders']).isnumeric():
                numSenders = int(requestData['numSenders'])

        if numMessages is None or failureRate is None or numSenders is None:
            resp = jsonify({
                'status': 'INVALID'
            })
            resp.status_code = 200
            simulationInitLock.release()
            return resp

        # Resets the sender stats counters
        resetSimulation()

        # Start producer thread
        producerThread = Producer(numMessages)
        producerThread.daemon = True
        producerThread.start()

        # Initialize and start sender threads
        senderThreads = []
        for i in range(numSenders):
            senderThread = Sender(failureRate)
            senderThreads.append(senderThread)
            senderThread.daemon = True
            senderThread.start()

        simulationInitLock.release()

        resp = jsonify({
            'status': 'SUCCESS'
        })
        resp.status_code = 200

        return resp

    return app


app = create_app({"TESTING": False})

CORS(
    app,
    origins="*",
    allow_headers=['content-type'],
    supports_credentials=False,
    methods=['GET', 'POST', 'DELETE']
)

if __name__ == '__main__':
    app.run()
