import asyncio
from . import Plugin


class DemoPlugin(Plugin):
    """
    Very simple demo plugin that prints "demo 1", "demo 2", etc
    in your i3bar. It demonstrates how to write asynchronous plugins.
    """
    def __init__(self):
        super().__init__()
        self.count = 0

    @property
    def status(self):
        """
        Return JSON-serializable output for i3bar. If in doubt, consult i3wm documentation
        or just fire up i3status to see the output format.

        If you have nothing to show, return empty list: []. Do not return None.

        :return: JSON-serializable array of statuses to be placed on i3bar.
        """
        return [{'name': 'demo', "full_text": f"demo {self.count}"}]

    async def run(self):
        """
        This async method will be started by Wonderbar. Just implement your
        event loop here.
        """
        while True:
            await asyncio.sleep(1)
            self.count = self.count+1
            self.refresh()
