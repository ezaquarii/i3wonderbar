import asyncio
import re
import subprocess


class TouchpadPlugin(object):
    """
    Show icon when touchpad is disabled.
    When touchpad is enabled, it shows nothing.
    """
    def __init__(self):
        super().__init__()
        self._id_regex = re.compile(r'[Tt]ouchpad.*id=(\d+).*pointer', re.UNICODE)
        self._enabled_regex = re.compile(r'Device Enabled.*:\s+(\d)', re.UNICODE)
        self._id = self._find_id()
        self._current_state = None
        self._refresh = None

    def register_refresh_callback(self, refresh):
        self._refresh = refresh

    @property
    def status(self):
        if self.enabled:
            return []
        else:
            # uses Font Awesome
            return [{"name": "touchpad", "full_text": "\uF05E", "color": "#FF0000"}]

    async def run(self):
        proc = await asyncio.create_subprocess_shell(
            f"stdbuf --output=0 xinput --watch-props {self._id}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        while True:
            raw_line = await proc.stdout.readline()
            if b'Device Enabled' in raw_line:
                line = raw_line.decode('utf8')
                self._on_new_line(line)

    def _find_id(self):
        output = subprocess.check_output(['xinput'])
        lines = output.decode('utf8').split('\n')
        for line in lines:
            match = self._id_regex.search(line)
            if match:
                return int(match.group(1))
        return None

    def _on_new_line(self, line):
        match = self._enabled_regex.search(line)
        if not match:
            return
        enabled = bool(int(match.group(1)))
        if enabled == self._current_state:
            return
        self._current_state = enabled
        if self._refresh:
            self._refresh(self)

    @property
    def enabled(self):
        output = subprocess.check_output(['xinput', '--list-props', str(self._id)])
        lines = output.decode('utf8').split('\n')
        for line in lines:
            if 'Device Enabled' in line:
                return bool(int(line[-1]))
        return False
