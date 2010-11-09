import rb
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

class SaaadPlugin (rb.Plugin):
    # Configuration constants for flask.
    APP_NAME = "saaad"
    DEBUG = True

    def __init__(self):
        rb.Plugin.__init__(self)
        self.shell = shell.props.shell_player.pause()
        
    def activate(self, shell):
        self.shell = shell
        self.
        app.run()
        
    def deactivate(self, shell):
        del self.shell
        
    def start_app(self):
        app = Flask(saaad)
        app.config.from_object(saaad)
        app.config.from_envvar('FLASKR_SETTINGS', silent=True)
        
    def do_action(self, action):
        value = action()
        return flask.jsonify(result=value)
        
    def do_action_with_result(self, action):
        value = action()
        return flask.jsonify(value)
    
    @app.route('/isplaying', methods=['GET'])
    def get_is_playing(self):
        '''Returns True if a song is being played.'''
        return do_action_with_result(self.props.shell_player.getPlaying)

    @app.route('/currentsong', methods=['GET'])
    def get_current_song(self):
        '''Returns the current song.'''
        if self.is_playing():
            uri = self.props.shell_player.getPlayingUri()
            song = self.props.shell_player.getSongProperties(uri)
            return jsonify(song)
        else:
            return jsonify()

    @app.route('/pause', methods=['POST'])
    def do_pause(self):
        return self.do_action(shell.props.shell_player.pause)
    
    @app.route('/play', methods=['POST'])
    def do_play():
        return self.do_action(shell.props.shell_player.play)

    @app.route('/stop', methods=['POST'])
    def do_stop():
        return self.do_action(shell.props.shell_player.stop)

    @app.route('/playpause', methods=['POST'])
    def do_playpause():
        return self.do_action(shell.props.shell_player.playpause)

    @app.route('/go_next', methods=['POST'])
    def do_next_song():
        return self.do_action(shell.props.shell_player.do_next)
    
    @app.route('/go_previous', methods=['POST'])
    def do_previous_song():
        return self.do_action(shell.props.shell_player.do_previous)

