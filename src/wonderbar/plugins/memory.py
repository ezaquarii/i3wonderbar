from wonderbar.theme import *

from . import Plugin


class MemoryPlugin(Plugin):
    def __init__(self):
        super().__init__()
        try:
            import psutil
            self._virtual_memory = psutil.virtual_memory
        except ModuleNotFoundError:
            self._virtual_memory = None

    @property
    def status(self):
        if not self._virtual_memory:
            return []
        else:
            mem = int(self._virtual_memory().percent)
            status = f"\uF2DB {mem}%"

            if mem < 50:
                color = COLOR_GOOD
            elif mem < 65:
                color = COLOR_AVERAGE
            elif mem < 80:
                color = COLOR_WARNING
            else:
                color = COLOR_BAD

            return [{"name": "memory", "full_text": status, "color": color}]

    async def run(self):
        pass
