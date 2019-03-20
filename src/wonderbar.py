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
import json
import sys

from wonderbar.plugins.network import NetworkPlugin
from wonderbar.plugins.touchpad import TouchpadPlugin
from wonderbar.plugins.memory import MemoryPlugin
from wonderbar.plugins.power import PowerPlugin
from wonderbar.plugins.i3status import I3Status


class Wonderbar(object):
    """
    This is a Wonderbar runtime engine. It collects statuses from registered
    plugins and continuously streams i3bar state to stdout.
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
    wbar.add_plugin(NetworkPlugin())
    wbar.add_plugin(I3Status(config=options.config))
    #w.add_plugin(DemoPlugin())

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(wbar.run())
    loop.run_forever()
