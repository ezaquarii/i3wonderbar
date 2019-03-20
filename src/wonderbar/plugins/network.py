from wonderbar.theme import *
from wonderbar.plugins import Plugin
from NetworkManager import NetworkManager, Wireless, Wired


class NetworkPlugin(Plugin):

    NO_CONNECTION_STATUS = []

    UNKNOWN_CONNECTION_STATUS = [{
        "name": "network",
        "full_text": f"\uF6FF?",
        "color": COLOR_GOOD
    }]

    WIRED_CONNECTION_STATUS = [{
        "name": "network",
        "full_text": f"\uF6FF",
        "color": COLOR_GOOD
    }]

    @staticmethod
    def get_status_color(signal):
        if signal > 70:
            return COLOR_GOOD
        elif signal > 60:
            return COLOR_AVERAGE
        elif signal > 30:
            return COLOR_WARNING
        else:
            return COLOR_BAD

    @property
    def status(self):
        connection = NetworkManager.PrimaryConnection
        if not connection:
            return self.NO_CONNECTION_STATUS

        devices = connection.Devices
        if len(devices) < 1:
            return self.UNKNOWN_CONNECTION_STATUS

        device = connection.Devices[0]
        if type(device) == Wireless:
            ap = device.ActiveAccessPoint
            signal = int(ap.Strength)
            return [{
                "name": "network",
                "full_text": f"\uF1EB {signal}% {ap.Ssid}",
                "color": self.get_status_color(signal)
            }]
        elif type(device) == Wired:
            return self.WIRED_CONNECTION_STATUS
        else:
            return self.UNKNOWN_CONNECTION_STATUS
