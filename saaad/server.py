'''Module with the Flask server actions.'''

import bottle
import multiprocessing

# Bottle application.
bottle.debug(True)
APP = bottle.Bottle()
APP_PROCESS = None

# Plugin object.
PLUGIN = None

def start_server():
    '''Starts the Flask server.'''
    if not PLUGIN:
        raise Exception("The plugin is still not loaded.")
    
    global APP_PROCESS
    func = lambda : bottle.run(app=APP, host="localhost", port="5000")
    APP_PROCESS = multiprocessing.Process(target=func)
    APP_PROCESS.daemon = True
    APP_PROCESS.start()
    
def stop_server():
    '''Stops the Flask server.'''
    global APP_PROCESS
    if not APP_PROCESS:
        raise Exception("The process is not running.")
    APP_PROCESS.terminate()
    APP_PROCESS = None
        
def do_simple(action):
    '''Execute an action and return only a single value.'''
    value = action()
    return {"result": value}
    
def do_with_result(action):
    '''Execute an action and return the result as a JSON map.'''
    value = action()
    return value
    
@APP.route("/test")
def test():
    '''Returns True if a song is being played.'''
    return "Funciona"
    
@APP.route("/isplaying")
def is_playing():
    '''Returns True if a song is being played.'''
    return do_simple(PLUGIN.get_is_playing)

@APP.route("/currentsong")
def current_song():
    '''Returns the current song data or an empty dictionary.'''
    return do_with_result(PLUGIN.get_current_song)

@APP.route("/pause")
def pause_song():
    '''Returns True if the current song was paused.'''
    return do_simple(PLUGIN.do_pause)

@APP.route("/play")
def play_song():
    '''Returns True if the current song started to play.'''
    return do_simple(PLUGIN.do_play)

@APP.route("/stop")
def stop_song():
    '''Returns True if the current song was stopped.'''
    return do_simple(PLUGIN.do_stop)

@APP.route("/playpause")
def playpause():
    '''Returns True if the current song alternated between play and pause.'''
    return do_simple(PLUGIN.do_playpause)

@APP.route("/go_next_song")
def next_song():
    '''Returns True if the next song started playing.'''
    return do_simple(PLUGIN.do_next_song)

@APP.route("/go_previous")
def previous_song():
    '''Returns True if the previous song started playing.'''
    return do_simple(PLUGIN.do_previous_song)
