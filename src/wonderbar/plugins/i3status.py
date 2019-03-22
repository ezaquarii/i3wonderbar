import asyncio
import json
import sys

from . import Plugin


class I3StatusPlugin(Plugin):
    """
    This plugin wraps i3status and forwards it's output to stdout.
    Use this plugin if you want to extend your existing i3status configuration.

    You need to configure your i3status separately.
    """
    def __init__(self, config):
        super().__init__()
        """
        :param config: Path to file with i3status configuration
        """
        self._cmd = f"i3status -c \'{config}\'"
        self._status = []

    @property
    def status(self):
        return self._status

    async def run(self):
        proc = await asyncio.create_subprocess_shell(
            self._cmd,
            stdout=asyncio.subprocess.PIPE,
        )
        while True:
            line = await proc.stdout.readline()
            if line == b'':
                print('Warning: i3status stdout pipe is closed! Stopping the plugin.', file=sys.stderr)
                proc.terminate()
                await proc.wait()
                return
            elif len(line) <= 2 or line.startswith(b'{'):
                continue
            else:
                strip_beginning = 1 if line.startswith(b',') else 0
                status = json.loads(line[strip_beginning:])
                self._status = status
                self.refresh()
