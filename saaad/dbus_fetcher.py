'''Module that obtains the shell player from DBus.'''

ROOT_NAME = 'org.freedesktop.DBus'
ROOT_PATH = '/org/freedesktop/DBus'
SHELL_NAME = 'org.gnome.Rhythmbox',
SHELL_PATH = '/org/gnome/Rhythmbox/Player'

class DBusFetcher:
    def __init__():
        # Get the dbus module.
        try:
            import dbus
            dbus_version = getattr(dbus, 'version', (0, 0, 0))
            if dbus_version >= (0, 41, 0) and dbus_version < (0, 80, 0):
                dbus.SessionBus()
                import dbus.glib
            elif dbus_version >= (0, 80, 0):
                from dbus.mainloop.glib import DBusGMainLoop
                DBusGMainLoop(set_as_default = True)
                dbus.SessionBus()
            else:
                print 'Please update python-dbus to 0.41.0 or newer.'
                raise
        except dbus.DBusException, error:
            print 'Unable to use DBus: %s' % str(error)

        # Set the state to reconnect.
        self.bus = None
        self.rb_shell = None
        self.module = dbus
        self.root = dbus.SessionBus().get_object(ROOT_NAME, ROOT_PATH)
    
    def reconnect(self):
        '''Attempt to reconnect if the bus object is still not initialized.'''
        self.bus = self.module.SessionBus()
        try:
            self.rb_shell = self.bus.get_object(SHELL_NAME, SHELL_PATH)
            return True
        except self.module.DBusException, error:
            self.rb_shell = None
            print 'A DBus error has occurred: %s' % str(error)
            return False
    
    def obtain_shell_player():
        '''Return the shell player or None, if a shell player was fetched.'''
        if self.is_name_active(SHELL_NAME):
            if self.rb_shell is None:
                self.reconnect()
        else:
            self.rb_shell = None        
        return self.rb_shell
    
    def is_name_active(self, name):
        '''Return True if the name is active on dbus.'''
        return bool(self.root.NameHasOwner(name))
