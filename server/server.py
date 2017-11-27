import logging
import sys 
import traceback
from twisted.python import log
import json

from flask import Flask 
from flask_socketio import SocketIO, send, emit
import numpy as np
from poap.controller import *
from poap.strategy import *
from pySOT import *

from controller_object import ControllerObject
from module_scraper import GetModuleClass
from pySOT_dictionary import PySOTDictionary
from pySOT_object import PySOTObject


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


def make_correction_to_data (parsed_json):
    if parsed_json['adaptive_sampling']['weights'] == -1:
        parsed_json['adaptive_sampling']['weights'] = None

@socketio.on('get_dict')
def sendingDict(msg):
    emit('recv_dict', json.dumps(class_dict))

@socketio.on('run')
def onMsgRun(msg):

    parsed_json = json.loads( msg )

    make_correction_to_data(parsed_json)
    
    class_dict = new_dict.get_dict()
    
    try:
        new_obj = PySOTObject(parsed_json, class_dict)
    except (ValueError, AttributeError) as e:
        emit('error_msg', e)
        print(e)
        return

    pySOTObj = new_obj.return_values()

    print(pySOTObj['data'].info)
    
    try:
        new_controller_object = ControllerObject(parsed_json, pySOTObj, class_dict)
    except (ValueError, AttributeError) as e:
        emit('error_msg', e)
        print(e)
        return
    
    controller = new_controller_object.get_controller()

    result = controller.run()

    print('Best value found: {0}'.format(result.value))
    print('Best solution found: {0}'.format(
        np.array_str(result.params[0], max_line_width=np.inf,
                    precision=5, suppress_small=True)))

    #Step 3
    import matplotlib.pyplot as plt

    # Extract function values from the controller
    fvals = np.array([o.value for o in controller.fevals])

    f, ax = plt.subplots()
    print(np.arange(0,pySOTObj['maxeval']))
    print(fvals)

    ax.plot(np.arange(0,pySOTObj['maxeval']), fvals, 'bo')  # Points
    ax.plot(np.arange(0,pySOTObj['maxeval']), np.minimum.accumulate(fvals), 'r-', linewidth=4.0)  # Best value found
    plt.xlabel('Evaluations')
    plt.ylabel('Function Value')
    plt.title(pySOTObj['data']
        .info)
    plt.show()

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    emit('abc',msg)

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    
    global new_dict
    new_dict = PySOTDictionary()

    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app, debug=True)