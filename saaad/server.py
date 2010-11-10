'''Module with the Flask server actions.'''

import multiprocessing
from flask import Flask, jsonify

APP_NAME = "saaad"

app = Flask(APP_NAME)
app.config.from_object(APP_NAME)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

class FlaskServer:
    '''
    Class that acts as a middle-man between the Flask server and the Plugin.
    '''
    # Configuration constants for flask.
    DEBUG = True

    def __init__(self, shell):
        self.app_process = None
        self.shell = shell
        
    def start(self):
        '''Starts the Flask server.'''
        self.app_process = multiprocessing.Process(target=app.run)
        self.app_process.daemon = True
        self.app_process.start()
        
    def stop(self):
        '''Stops the Flask server.'''
        self.app_process.terminate()
        self.app_process = None
        
def do(action):
    '''Execute an action and return only a single value.'''
    value = action()
    return jsonify(result=value)
    
def do_with_result(action):
    '''Execute an action and return the result as a JSON map.'''
    value = action()
    return jsonify(value)
