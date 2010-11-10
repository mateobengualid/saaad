'''Module with the Spooky Action At A Distance plugin for Rhythmbox.'''

import rb
import multiprocessing
from flask import Flask, jsonify, logging

APP_NAME = "saaad"

app = Flask(APP_NAME)
app.config.from_object(APP_NAME)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

class SaaadPlugin (rb.Plugin):
    '''
    Plugin that exposes the player operations with HTTP operations using
    Flask.
    '''
    # Configuration constants for flask.
    DEBUG = True

    def __init__(self):
        rb.Plugin.__init__(self)
        self.shell = None
        self.app_process = None
        
    def activate(self, shell):
        '''Activate the plugin.
        
        Activate the plugin by setting the shell and starting the server. This
        method must be overwritten, as it is indicated by the Rhythmbox
        documentation.
        '''
        self.app_process = multiprocessing.Process(target=app.run)
        self.app_process.daemon = True
        self.app_process.start()
        self.shell = shell
        
    def deactivate(self, shell):
        '''Deactivate the plugin.
        
        Deactivate the server. This includes stopping the server and disposing
        the shell. This method must be overwritten, as it is indicated by the
        Rhythmbox documentation.
        '''
        self.app_process.terminate()
        self.app_process = None
        del self.shell
                
    def do_action(self, action):
        '''Execute an action on the player that returns only a single value.'''
        value = action()
        print value
        return jsonify(result=value)
        
    def do_action_with_result(self, action):
        '''Execute an action on the player that returns a dictionary.'''
        value = action()
        return jsonify(value)
    
    @app.route('/isplaying', methods=['GET'])
    def get_is_playing(self):
        '''Returns True if a song is being played.'''
        return app.make_response("Hola")
        #logger.info(self.shell)
        #logger.info(self.shell.props)
        #logger.info(self.shell.props.shell_player)
        #logger.info(self.shell.props.shell_player.getPlaying)
        #logger.info(self.shell.props.shell_player.getPlaying())
        #action = self.shell.props.shell_player.getPlaying
        #return self.do_action_with_result(action)
        #return "Something"

    @app.route('/currentsong', methods=['GET'])
    def get_current_song(self):
        '''Returns the current song data or an empty dictionary.'''
        if self.shell.props.shell_player.getPlaying():
            uri = self.shell.props.shell_player.getPlayingUri()
            song = self.shell.props.shell_player.getSongProperties(uri)
            return jsonify(song)
        else:
            return jsonify()

    @app.route('/pause', methods=['POST'])
    def do_pause(self):
        return self.do_action(self.shell.props.shell_player.pause)
    
    @app.route('/play', methods=['POST'])
    def do_play(self):
        return self.do_action(self.shell.props.shell_player.play)

    @app.route('/stop', methods=['POST'])
    def do_stop(self):
        return self.do_action(self.shell.props.shell_player.stop)

    @app.route('/playpause', methods=['POST'])
    def do_playpause(self):
        return self.do_action(self.shell.props.shell_player.playpause)

    @app.route('/go_next', methods=['POST'])
    def do_next_song(self):
        return self.do_action(self.shell.props.shell_player.do_next)
    
    @app.route('/go_previous', methods=['POST'])
    def do_previous_song(self):
        return self.do_action(self.shell.props.shell_player.do_previous)
