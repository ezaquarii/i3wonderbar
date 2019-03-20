import asyncio
import json


class I3Status(object):
    """
    This plugin wraps i3status and forwards it's output to stdout.
    Use this plugin if you want to extend your existing i3status configuration.

    You need to configure your i3status separately.
    """
    def __init__(self, config):
        """
        :param config: Path to file with i3status configuration
        """
        self._cmd = f"i3status -c \'{config}\'"
        self._status = []
        self._refresh = None

    def register_refresh_callback(self, refresh):
        self._refresh = refresh

    @property
    def status(self):
        return self._status

    async def run(self):
        proc = await asyncio.create_subprocess_shell(
            self._cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        while True:
            line = await proc.stdout.readline()
            if len(line) <= 2 or line.startswith(b'{'):
                continue
            else:
                strip_beginning = 1 if line.startswith(b',') else 0
                status = json.loads(line[strip_beginning:])
                self._status = status
                if self._refresh:
                    self._refresh(self)
