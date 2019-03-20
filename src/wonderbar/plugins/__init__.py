
class Plugin(object):
    """Base plugin class. All plugins should implement this interface."""

    def __init__(self):
        self.__refresh = None

    def register_refresh_callback(self, refresh):
        """
        This method is called by Wonderbar to inject update trigger.
        You should call on_update() when your plugin state changes,
        forcing Wonderbar to refresh.

        Refresh callback accepts single argument - the plugin instance.
        This can be used during debugging.

        :param refresh: function(plugin)
        """
        self.__refresh = refresh

    @property
    def status(self):
        return []

    def refresh(self):
        if self.__refresh:
            self.__refresh()

    async def run(self):
        """
        This is a place for plugin sync loop. To send asynchronous
        updates by calling self.refresh() to force status bar
        redraw with new status information.
        """
        pass
