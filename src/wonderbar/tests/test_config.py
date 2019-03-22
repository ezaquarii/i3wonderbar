import os.path
import tempfile
import unittest

from . import get_fixture_path
from wonderbar.core import Config


class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.config_file = get_fixture_path("config.ini")
        self.config = Config()
        self.config.load(self.config_file)

    def test_plugins_are_loaded(self):
        self.assertEqual(2, len(self.config.plugins))
        expected_plugins = {"demo",
                            "power"}
        self.assertEqual(expected_plugins, set(self.config.plugins))

    def test_general_config_is_loaded(self):
        self.assertEqual(10, self.config.interval)


class TestDefaultConfig(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.config_file = get_fixture_path("empty_config.ini")
        self.config = Config()
        self.config.load(self.config_file)

    def test_plugins_are_loaded(self):
        self.assertEqual(2, len(self.config.plugins))

    def test_general_config_is_loaded(self):
        self.assertEqual(Config.DEFAULT_INTERVAL, self.config.interval)


class TestWriteConfig(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'config.ini')
        self.config = Config()
        self.config.interval = 15
        self.config.plugins = ['demo']
        self.config.save(self.config_file)

    def test_saved_file_exists(self):
        self.assertTrue(os.path.isfile(self.config_file))

    def test_saved_contents(self):
        loaded_config = Config()
        loaded_config.load(self.config_file)
        self.assertEqual(self.config.interval, loaded_config.interval)
        self.assertEqual(self.config.plugins, loaded_config.plugins)
