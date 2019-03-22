import asyncio
from collections import deque
from wonderbar.theme import *

from . import Plugin

class PowerPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self._times = deque()
        self._avg_time_left = 0
        self._power_left = 100
        self._is_charging = None

        try:
            import psutil
            self._sensors_battery = psutil.sensors_battery
        except ModuleNotFoundError:
            self._sensors_battery = None

    def update_battery_status(self):
        battery = self._sensors_battery()
        self._times.append(int(battery.secsleft))
        if len(self._times) > 5:
            self._times.popleft()
        self._avg_time_left = int(sum(self._times)/len(self._times))
        self._power_left = int(battery.percent)
        should_refresh_immediately = self._is_charging != battery.power_plugged
        self._is_charging = battery.power_plugged
        return should_refresh_immediately

    @property
    def status(self):
        if not self._sensors_battery:
            return []
        else:
            formatted_time_left = "{:02}:{:02}".format(self._avg_time_left // 3600, self._avg_time_left % 3600 // 60)
            if self._is_charging:
                icon = '\uF0E7'
                color = COLOR_GOOD
            elif self._power_left >= 80:
                icon = '\uF240'
                color = COLOR_GOOD
            elif self._power_left >= 60:
                icon = '\uF241'
                color = COLOR_AVERAGE
            elif self._power_left >= 40:
                icon = '\uF242'
                color = COLOR_AVERAGE
            elif self._power_left >= 20:
                icon = '\uF243'
                color = COLOR_WARNING
            else:
                icon = '\uF244'
                color = COLOR_BAD
            if self._is_charging:
                status = f"{icon} {self._power_left}%"
            else:
                status = f"{icon} {self._power_left}% {formatted_time_left}"

            return [{"name": "power", "full_text": status, "color": color}]

    async def run(self):
        while True:
            refresh = self.update_battery_status()
            if refresh:
                self.refresh()
            await asyncio.sleep(5)
