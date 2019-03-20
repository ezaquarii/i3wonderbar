from wonderbar.theme import *


class MemoryPlugin(object):
    def __init__(self):
        self._refresh = None
        try:
            import psutil
            self._virtual_memory = psutil.virtual_memory
        except ModuleNotFoundError:
            self._virtual_memory = None

    def register_refresh_callback(self, refresh):
        self._refresh = refresh

    @property
    def status(self):
        if not self._virtual_memory:
            return []
        else:
            mem = self._virtual_memory().percent
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