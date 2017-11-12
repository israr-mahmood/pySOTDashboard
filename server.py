from flask import Flask 
from flask_socketio import SocketIO, send, emit
from threading import Thread

import json
import time

from poap.strategy import FixedSampleStrategy
from poap.strategy import CheckWorkerStrategy
from poap.strategy import InputStrategy

from pySOT import *
from poap.controller import SerialController, ThreadController, BasicWorkerThread
import numpy as np

from pySOT_obj import pySOT_obj
from mod_scraper import get_mod_class
from pySOT_dict import pySOT_class_dict
from controller_obj import controller_obj

from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


def checkering(msg):
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(str(msg))
    print(msg.params)
    print(msg._status)
    print(msg.value)
    print(msg.status)
    if msg.status != 'pending':
        while 1:
            pass
    return 1

def make_correction_to_data (parsed_json):
    if parsed_json['adaptive_sampling']['weights'] == -1:
        parsed_json['adaptive_sampling']['weights'] = None

@socketio.on('run')
def onMsgRun(msg):
    #msg = '{ "optimization_problem" : {"function" : "Ackley" , "dim" : 10} , "experimental_design" : { "function" : "SymmetricLatinHypercube" , "dim" : 10, "npts" : 21 } , "surrogate_model" : { "function" : "RBFInterpolant" , "maxp" : 500 , "tail" : "LinearTail" , "kernel" : "CubicKernel" } , "adaptive_sampling" : { "function" : "CandidateDYCORS" , "numcand" : 100 , "weights" : -1 } , "controller" : { "function" : "SerialController" } , "strategy" : { "function" : "SyncStrategyNoConstraints" , "nsamples" : 1 , "proj_fun" : "projection" } }';

    print(msg)
    parsed_json = json.loads( msg )

    make_correction_to_data(parsed_json)

    print(parsed_json)

    #from obj_make import pySOT_obj, pySOT_class_dict
    new_dict = pySOT_class_dict()
    [sucess, class_dict] = new_dict.get_dict()
    if not sucess:
        print(msg+'\n\n\n')
        emit('error_msg', class_dict)
        return
    print('got out of dict')

    new_obj = pySOT_obj(parsed_json, class_dict)
    [sucess, msg] = new_obj.run()
    print('goof here')
    if not sucess:
        print('not good')
        print(msg+'\n\n\n')
        emit('error_msg', msg)
        return
    print('done obj')
    pySOTObj = new_obj.return_values()

    print(pySOTObj['data'].info)

    print('controller start')
    new_controller = controller_obj(parsed_json, pySOTObj, [checkering,], class_dict)
    print('controller init')
    [sucess, controller] = new_controller.get_controller()
    print('controller done')
    if not sucess:
        print(controller+'\n\n\n')
        emit('error_msg', controller)
        return

    result = controller.run()

    # Print the final result
    print('Best value found: {0}'.format(result.value))
    print('Best solution found: {0}'.format(
        np.array_str(result.params[0], max_line_width=np.inf,
                    precision=5, suppress_small=True)))

    #Step 3
    import matplotlib.pyplot as plt

    # Extract function values from the controller
    fvals = np.array([o.value for o in controller.fevals])

    f, ax = plt.subplots()
    ax.plot(np.arange(0,pySOTObj['maxeval']), fvals, 'bo')  # Points
    ax.plot(np.arange(0,pySOTObj['maxeval']), np.minimum.accumulate(fvals), 'r-', linewidth=4.0)  # Best value found
    plt.xlabel('Evaluations')
    plt.ylabel('Function Value')
    plt.title(pySOTObj['data']
        .info)
    plt.show()

    print('ch shu')
    print(class_dict)

    print(' ')
    print(json.dumps(class_dict))

    return

@socketio.on('terminate_')
def onMsgTerminate(msg):
    print(msg)
    reactor.callInThread(self.manager.terminate)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    #send(msg , broadcast=True)
    emit('abc',msg)
    i=0
    while i<10:
        print('the happeing ' + str(i))
        i+=1
        sleep(1)

if __name__ == '__main__':
    import sys
    from twisted.python import log

    log.startLogging(sys.stdout)
    import logging

    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app, debug=True)