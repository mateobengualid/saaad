'''Module with the Bottle server actions.'''

import bottle
import multiprocessing

# Bottle application.
bottle.debug(True)
APP = bottle.Bottle()
APP_PROCESS = None

# Plugin object.
PLUGIN = None

def start_server():
    '''Starts the Bottle server.'''
    if not PLUGIN:
        raise Exception("The plugin is still not loaded.")
    global APP_PROCESS
    func = lambda : bottle.run(app=APP, host="localhost", port="5000")
    APP_PROCESS = multiprocessing.Process(target=func)
    APP_PROCESS.daemon = True
    APP_PROCESS.start()
    
def stop_server():
    '''Stops the Bottle server.'''
    global APP_PROCESS
    if not APP_PROCESS:
        raise Exception("The process is not running.")
    try:
        APP_PROCESS.terminate()
    except OSError:
        pass

    APP_PROCESS = None
        
def as_value(value):
    '''Return a dictionary with that single value.'''
    return {"result": value}
    
@APP.route("/test")
def test():
    '''Returns True if a song is being played.'''
    return "Funciona"
    
@APP.route("/isplaying")
def is_playing():
    '''Returns True if a song is being played.'''
    return as_value(PLUGIN.get_is_playing())

@APP.route("/currentsong")
def current_song():
    '''Returns the current song data or an empty dictionary.'''
    return PLUGIN.get_current_song()

@APP.route("/pause")
def pause_song():
    '''Returns True if the current song was paused.'''
    return as_value(PLUGIN.do_pause())

@APP.route("/play")
def play_song():
    '''Returns True if the current song started to play.'''
    return as_value(PLUGIN.do_play())

@APP.route("/stop")
def stop_song():
    '''Returns True if the current song was stopped.'''
    return as_value(PLUGIN.do_stop())

@APP.route("/playpause")
def playpause():
    '''Returns True if the current song alternated between play and pause.'''
    return as_value(PLUGIN.do_playpause())

@APP.route("/go_next_song")
def next_song():
    '''Returns True if the next song started playing.'''
    return as_value(PLUGIN.do_next_song())

@APP.route("/go_previous")
def previous_song():
    '''Returns True if the previous song started playing.'''
    return as_value(PLUGIN.do_previous_song())
