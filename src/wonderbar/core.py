import asyncio
import importlib
import json
import sys

from .plugins import Plugin


def import_plugin(name):
    try:
        plugin_package = importlib.import_module(f"..plugins.{name}", __name__)
        for key, plugin_class in plugin_package.__dict__.items():
            plugin_name = key.lower()
            if plugin_name.startswith(name) and plugin_name.endswith('plugin') and issubclass(plugin_class, Plugin):
                return plugin_class
    except ModuleNotFoundError:
        pass
    return None


class Config(object):

    DEFAULT_INTERVAL = 5
    DEFAULT_PLUGINS = ['touchpad', 'memory', 'power', 'network', 'i3status']

    def __init__(self):
        self.plugins = Config.DEFAULT_PLUGINS
        self.interval = Config.DEFAULT_INTERVAL

    def __str__(self):
        from configparser import ConfigParser
        parser = ConfigParser(allow_no_value=True)

        parser.add_section('general')
        parser.set('general', 'interval', str(self.interval))

        parser.add_section('plugins')
        for plugin in self.plugins:
            parser.set('plugins', plugin)

        from io import StringIO
        buf = StringIO()
        parser.write(buf)
        return buf.getvalue()

    def save(self, config_file):
        contents = self.__str__()
        with open(config_file, 'w') as f:
            f.write(contents)

    def load(self, config_file):
        parser = self._parse(config_file)
        self._load_general(parser)
        self._load_plugins(parser)

    def _parse(self, config_file):
        from configparser import ConfigParser, ParsingError
        parser = ConfigParser(allow_no_value=True)
        result = parser.read(config_file)
        if len(result) == 0:
            raise ParsingError("Cannot load file %s" % config_file)
        return parser

    def _load_plugins(self, parser):
        if 'plugins' in parser:
            section = parser['plugins']
            self.plugins = [key for key in section.keys()]

    def _load_general(self, parser):
        if 'general' in parser:
            section = parser['general']
            if 'interval' in section:
                self.interval = int(section.get('interval'))


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
            _ = asyncio.ensure_future(plugin.run())

        while True:
            self.on_update(self)
            await asyncio.sleep(self._interval)

    def on_update(self, plugin):
        all_statuses = sum([p.status for p in self._plugins], [])
        status = json.dumps(all_statuses)
        print(f",{status}\n", file=sys.stdout, flush=True)
