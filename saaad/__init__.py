'''Module with the Spooky Action At A Distance plugin for Rhythmbox.'''

import rb
import server

class SaaadPlugin (rb.Plugin):
    '''
    Plugin that exposes the player operations with HTTP operations using
    Flask.
    '''

    def __init__(self):
        rb.Plugin.__init__(self)
        self.shell = None
        
    def activate(self, shell):
        '''Activate the plugin.
        
        Activate the plugin by setting the shell and starting the server. This
        method must be overwritten, as it is indicated by the Rhythmbox
        documentation.
        '''
        self["shell"] = shell
        server.PLUGIN = self
        server.start_server()
        
    def deactivate(self, shell):
        '''Deactivate the plugin.
        
        Deactivate the server. This includes stopping the server and disposing
        the shell. This method must be overwritten, as it is indicated by the
        Rhythmbox documentation.
        '''
        server.stop_server()
        server.PLUGIN = None        
        del self.shell
        
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
        '''Returns True if the song being played is paused.'''
        return self.shell.props.shell_player.pause()

    def do_play(self):
        '''Returns True if the song being played is played.'''
        return self.shell.props.shell_player.play()

    def do_stop(self):
        '''Returns True if the song being played is stopped.'''
        return self.shell.props.shell_player.stop()

    def do_playpause(self):
        '''Returns True if the song alternated between play and pause state.'''
        return self.shell.props.shell_player.playpause()

    def do_next_song(self):
        '''Returns True if the next song starts playing.'''
        return self.shell.props.shell_player.do_next()

    def do_previous_song(self):
        '''Returns True if the previous song starts playing.'''
        return self.shell.props.shell_player.do_previous()
