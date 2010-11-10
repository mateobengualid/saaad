'''Module with the Flask server actions.'''

import multiprocessing
from flask import Flask, jsonify, logging

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
        
def do_action(action):
    '''Execute an action and return only a single value.'''
    value = action()
    return jsonify(result=value)
    
def do_action_with_result(action):
    '''Execute an action and return the result as a JSON map.'''
    value = action()
    return jsonify(value)
    
@app.route('/isplaying', methods=['GET'])
def get_is_playing():
    '''Returns True if a song is being played.'''
    action = self.shell.props.shell_player.getPlaying
    return self.do_action_with_result(action)

@app.route('/currentsong', methods=['GET'])
def get_current_song():
    '''Returns the current song data or an empty dictionary.'''
    if self.shell.props.shell_player.getPlaying():
        uri = self.shell.props.shell_player.getPlayingUri()
        song = self.shell.props.shell_player.getSongProperties(uri)
        return jsonify(song)
    else:
        return jsonify()

@app.route('/pause', methods=['POST'])
def do_pause():
    return self.do_action(self.shell.props.shell_player.pause)

@app.route('/play', methods=['POST'])
def do_play():
    return self.do_action(self.shell.props.shell_player.play)

@app.route('/stop', methods=['POST'])
def do_stop():
    return self.do_action(self.shell.props.shell_player.stop)

@app.route('/playpause', methods=['POST'])
def do_playpause():
    return self.do_action(self.shell.props.shell_player.playpause)

@app.route('/go_next', methods=['POST'])
def do_next_song():
    return self.do_action(self.shell.props.shell_player.do_next)

@app.route('/go_previous', methods=['POST'])
def do_previous_song():
    return self.do_action(self.shell.props.shell_player.do_previous)
