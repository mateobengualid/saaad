'''Module with the Flask server actions.'''

import os
import signal
import threading
from flask import Flask, jsonify

# Flask application.
APP = Flask("server")
APP_THREAD = None

# Flask constants.
APP.config['DEBUG'] = True

# Plugin object.
PLUGIN = None

def start_server():
    '''Starts the Flask server.'''
    if not PLUGIN:
        raise Exception("The plugin is still not loaded.")
    
    global APP_THREAD
    APP_THREAD = threading.Thread(target=APP.run)
    APP_THREAD.daemon = True
    APP_THREAD.start()
    
def stop_server():
    '''Stops the Flask server.'''
    global APP_THREAD
    if not APP_THREAD:
        raise Exception("The process is not running.")
    try:
        os.kill(APP_THREAD, signal.SIGKILL)
    except OSError:
        pass

    APP_THREAD = None
        
def do_simple(action):
    '''Execute an action and return only a single value.'''
    value = action()
    return jsonify(result=value)
    
def do_with_result(action):
    '''Execute an action and return the result as a JSON map.'''
    value = action()
    return jsonify(value)
    
@APP.route("/isplaying", methods=['GET'])
def is_playing():
    '''Returns True if a song is being played.'''
    return do_simple(PLUGIN.get_is_playing)

@APP.route("/currentsong", methods=['GET'])
def current_song():
    '''Returns the current song data or an empty dictionary.'''
    return do_with_result(PLUGIN.get_current_song)

@APP.route("/pause", methods=['POST'])
def pause_song():
    '''Returns True if the current song was paused.'''
    return do_simple(PLUGIN.do_pause)

@APP.route("/play", methods=['POST'])
def play_song():
    '''Returns True if the current song started to play.'''
    return do_simple(PLUGIN.do_play)

@APP.route("/stop", methods=['POST'])
def stop_song():
    '''Returns True if the current song was stopped.'''
    return do_simple(PLUGIN.do_stop)

@APP.route("/playpause", methods=['POST'])
def playpause():
    '''Returns True if the current song alternated between play and pause.'''
    return do_simple(PLUGIN.do_playpause)

@APP.route("/go_next_song", methods=['POST'])
def next_song():
    '''Returns True if the next song started playing.'''
    return do_simple(PLUGIN.do_next_song)

@APP.route("/go_previous", methods=['POST'])
def previous_song():
    '''Returns True if the previous song started playing.'''
    return do_simple(PLUGIN.do_previous_song)
