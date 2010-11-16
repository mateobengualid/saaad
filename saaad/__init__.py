'''Module with the Spooky Action At A Distance plugin for Rhythmbox.'''

import rb
import server

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
        self.server = server.FlaskServer()
        self.hook_functions()
        
    def activate(self, shell):
        '''Activate the plugin.
        
        Activate the plugin by setting the shell and starting the server. This
        method must be overwritten, as it is indicated by the Rhythmbox
        documentation.
        '''
        self.shell = shell
        self.server.start()
        
    def deactivate(self, shell):
        '''Deactivate the plugin.
        
        Deactivate the server. This includes stopping the server and disposing
        the shell. This method must be overwritten, as it is indicated by the
        Rhythmbox documentation.
        '''
        self.server.stop()
        del self.shell
        
    def hook_functions(self):  
        '''Hook the local functions to the Flask server.
        
        This is the most "unlike the rest" of the class functions. I'm quite
        noob, so any suggestion is more than welcome.
        '''
        isplaying = lambda : server.do(self.get_is_playing())
        server.app.add_url_rule(rule='/isplaying', view_func=isplaying,
            methods=['GET'])
        
        currentsong = lambda : server.do_with_result(self.get_current_song())
        server.app.add_url_rule(rule='/currentsong', view_func=currentsong,
            methods=['GET'])
        
        pause = lambda : server.do(self.do_pause())
        server.app.add_url_rule(rule='/pause', view_func=pause,
            methods=['POST'])

        play = lambda : server.do(self.do_play())
        server.app.add_url_rule(rule='/play', view_func=play,
            methods=['POST'])
        
        stop = lambda : server.do(self.do_stop())
        server.app.add_url_rule(rule='/stop', view_func=stop,
            methods=['POST'])

        playpause = lambda : server.do(self.do_playpause())
        server.app.add_url_rule(rule='/playpause', view_func=playpause,
            methods=['POST'])
            
        gonext = lambda : server.do(self.do_next_song())
        server.app.add_url_rule(rule='/go_next', view_func=gonext,
            methods=['POST'])

        goprevious = lambda : server.do(self.do_previous_song())
        server.app.add_url_rule(rule='/go_previous', view_func=goprevious,
            methods=['POST'])
        
    def get_is_playing(self):
        '''Returns True if a song is being played.'''
        return self.shell.props.shell_player.getPlaying()

    def get_current_song(self):
        '''Returns the current song data or an empty dictionary.'''
        if self.shell.props.shell_player.getPlaying():
            uri = self.shell.props.shell_player.getPlayingUri()
            song = self.shell.props.shell_player.getSongProperties(uri)
            return song
        else:
            return {}
            
    def do_pause(self):
        return self.shell.props.shell_player.pause()

    def do_play(self):
        return self.shell.props.shell_player.play()

    def do_stop(self):
        return self.shell.props.shell_player.stop()

    def do_playpause(self):
        return self.shell.props.shell_player.playpause()

    def do_next_song(self):
        return self.shell.props.shell_player.do_next()

    def do_previous_song(self):
        return self.shell.props.shell_player.do_previous()
