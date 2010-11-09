import rb
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

class SaaadPlugin (rb.Plugin):
    def __init__(self):
        rb.Plugin.__init__(self)
        self.shell = shell.props.shell_player.pause()
        
    def activate(self, shell):
        self.shell = shell
        
    def deactivate(self, shell):
        del self.shell
        
    def do_action(self, action):
        value = action()
        return render_template('show_result.html', result=value)
    
    @app.route('/isplaying', methods=['GET'])
    def get_is_playing(self):
        '''Returns if it is playing.'''
        if self.is_playing():
            uri = self.iface.getPlayingUri()
            song = self.rbshell.getSongProperties(uri)

            return songretriever.Song(song['artist'],
                                      song['album'],
                                      song['title'])

    @app.route('/currentsong', methods=['GET'])
    def get_current_song(self):
        '''Returns the current song.'''
        if self.is_playing():
            uri = self.iface.getPlayingUri()
            song = self.getSongProperties(uri)

            return songretriever.Song(song['artist'],
                                      song['album'],
                                      song['title'])

    @app.route('/pause', methods=['POST'])
    def do_pause(self):
        return self.do_action(shell.props.shell_player.pause)
    
    @app.route('/play', methods=['POST'])
    def do_play():
        return self.do_action(shell.props.shell_player.play)

    @app.route('/stop', methods=['POST'])
    def do_play():
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

