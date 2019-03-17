#!/usr/bin/env python3

# This file is Wonderbar - a hackable i3status replacement for i3 window manager
# 
# Copyright (C) 2019 Chris Narkiewicz <hello@ezaquarii.com>
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Wonderbar.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import asyncio
from datetime import timedelta
import json
import re
import subprocess
import sys


COLOR_GOOD = "#00FF00"
COLOR_AVERAGE = "#FFFF00"
COLOR_WARNING = "#FF9900"
COLOR_BAD = "#FF0000"

class DemoPlugin(object):
    """
    Very simple demo plugin that prints "demo 1", "demo 2", etc
    in your i3bar. It demonstrates how to write asynchronous plugins.
    """
    def __init__(self):
        self._refresh = None
        self.count = 0

    def register_refresh_callback(self, refresh):
        """
        This method is called by Wonderbar to inject update trigger.
        You should call on_update() when your plugin state changes,
        forcing Wonderbar to refresh.

        Refresh callback accepts single argument - the plugin instance.
        This can be used during debugging.

        :param refresh: function(plugin)
        """
        self._refresh = refresh

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
            self._refresh(self)


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
            status = f"\uF2DB{mem}%"

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


class PowerPlugin(object):
    def __init__(self):
        self._refresh = None
        try:
            import psutil
            self._sensors_battery = psutil.sensors_battery
        except ModuleNotFoundError:
            self._sensors_battery = None

    def register_refresh_callback(self, refresh):
        self._refresh = refresh

    @property
    def status(self):
        if not self._sensors_battery:
            return []
        else:
            battery = self._sensors_battery()
            time_left = str(timedelta(seconds=battery.secsleft))[:-3]
            power_left = int(battery.percent)

            if battery.power_plugged:
                icon = '\uF0E7'
                color = COLOR_GOOD
            elif power_left >= 80:
                icon = '\uF240'
                color = COLOR_GOOD
            elif power_left >= 60:
                icon = '\uF241'
                color = COLOR_AVERAGE
            elif power_left >= 40:
                icon = '\uF242'
                color = COLOR_AVERAGE
            elif power_left >= 20:
                icon = '\uF243'
                color = COLOR_WARNING
            else:
                icon = '\uF244'
                color = COLOR_BAD

            if battery.power_plugged:
                status = f"{icon}{power_left}%"
            else:
                status = f"{icon}{power_left}% {time_left}"

            return [{"name": "memory", "full_text": status, "color": color}]

    async def run(self):
        pass


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


class Wonderbar(object):
    """
    This is main Wonderbar engine. It collects statuses from registered plugins and
    continuously streams i3bar state to stdout.
    """
    def __init__(self, interval):
        self.i3_status = []
        self.touchpad_enabled = True
        self._interval = interval
        self._plugins = []

    def add_plugin(self, plugin):
        self._plugins.append(plugin)

    async def run(self):
        print('{"version":1}[[]', flush=True) # this is required by i3bar

        for plugin in self._plugins:
            plugin.register_refresh_callback(lambda plugin: self.on_update(plugin))
            asyncio.ensure_future(plugin.run())

        while True:
            self.on_update(self)
            await asyncio.sleep(self._interval)

    def on_update(self, plugin):
        all = sum([plugin.status for plugin in self._plugins], [])
        status = json.dumps(all)
        print(f",{status}\n", file=sys.stdout, flush=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, help="i3status config file.")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Update interval.")
    options = parser.parse_args()

    wbar = Wonderbar(interval=options.interval)
    wbar.add_plugin(TouchpadPlugin())
    wbar.add_plugin(MemoryPlugin())
    wbar.add_plugin(PowerPlugin())
    wbar.add_plugin(I3Status(config=options.config))
    #w.add_plugin(DemoPlugin())

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(wbar.run())
    loop.run_forever()
