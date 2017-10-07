from flask import Flask 
from flask_socketio import SocketIO, send
from threading import Thread



import json
import time

from poap.strategy import FixedSampleStrategy
from poap.strategy import CheckWorkerStrategy
from poap.strategy import InputStrategy
from poap.controller import ThreadController
from poap.controller import BasicWorkerThread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


def objective(x):
    time.sleep(1)
    return (x-0.123)*(x-0.123)

def init_controller():
    samples = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    controller = ThreadController()
    strategy = FixedSampleStrategy(samples)
    strategy = CheckWorkerStrategy(controller, strategy)
    controller.strategy = strategy

    for _ in range(5):
        worker = BasicWorkerThread(controller, objective)
        controller.launch_worker(worker)
    return controller


class Manager(InputStrategy,Thread):

    def __init__(self, controller, strategy = None):
        print('thread is up----------------------------------------')
        Thread.__init__(self)
        print('thread init running')
        if strategy is None:
            strategy = controller.strategy
        InputStrategy.__init__(self, controller, strategy)
        controller.strategy = self
        print('thread init complete--------------------------------')

    def notify(self, msg):
        print(msg)
        #reactor.callFromThread(self.server.send_notify, msg)
        send(msg, broadcast=True)

    def on_complete(self, rec):
        print('Module run complet---------------------------------')
        self.notify("Completed: {0} -> {1}".format(rec.params, rec.value))
        print('Module complete executed---------------------------')

    def on_kill(self, rec):
        self.notify("Killed: {0}".format(rec.params))

    def on_terminate(self, rec):
        self.notify("Terminating")

    def run(self):
        print('starting new module--------------------------------')
        #self.server = server
        result = self.controller.run()
        if result is None:
            self.notify("No result")
        else:
            self.notify("Result: {0} -> {1}".format(
                result.params, result.value))
        print('Module up and running------------------------------')

@socketio.on('c_connect')
def onConnect(msg):
    print('Message: ' + msg)
    send(msg)

def onMessage(payload, isBinary):
    if isBinary:
        return
        pass

    handlers = {
        'run': self.onMsgRun,
        'terminate': self.onMsgTerminate
    }
    print("Text message received: {0}".format(payload.decode('utf8')))
    msg = json.loads(payload.decode('utf8'))
    handlers[msg['type'].decode('utf8')](msg)

manager = None

@socketio.on('run_')
def onMsgRun(msg):
    print(msg)
    manager = Manager(init_controller())
    #reactor.callInThread(self.manager.run, self)
    manager.run()

@socketio.on('terminate_')
def onMsgTerminate(msg):
    print(msg)
    reactor.callInThread(self.manager.terminate)




@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('this_event')
def handleMessage(msg):
    print('Message1000: ' + msg)



if __name__ == '__main__':
    import sys
    from twisted.python import log

    log.startLogging(sys.stdout)
    import logging

    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app, debug=True)






 