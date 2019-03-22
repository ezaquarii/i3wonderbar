import unittest
from wonderbar.core import import_plugin


class TestImportPlugins(unittest.TestCase):

    def test_import_non_existing_plugin(self):
        plugin = import_plugin("non_existing_plugin")
        self.assertIsNone(plugin)

    def test_import_demo_plugin(self):
        plugin = import_plugin('demo')
        from wonderbar.plugins.demo import DemoPlugin
        self.assertIs(plugin, DemoPlugin)

    def test_import_network_plugin(self):
        plugin = import_plugin('network')
        from wonderbar.plugins.network import NetworkPlugin
        self.assertIs(plugin, NetworkPlugin)

    def test_import_i3status_plugin(self):
        plugin = import_plugin('i3status')
        from wonderbar.plugins.i3status import I3StatusPlugin
        self.assertIs(plugin, I3StatusPlugin)

    def test_import_memory_plugin(self):
        plugin = import_plugin('memory')
        from wonderbar.plugins.memory import MemoryPlugin
        self.assertIs(plugin, MemoryPlugin)

    def test_import_power_plugin(self):
        plugin = import_plugin('power')
        from wonderbar.plugins.power import PowerPlugin
        self.assertIs(plugin, PowerPlugin)

    def test_import_touchpad_plugin(self):
        plugin = import_plugin('touchpad')
        from wonderbar.plugins.touchpad import TouchpadPlugin
        self.assertIs(plugin, TouchpadPlugin)
