from os.path import join, abspath, dirname


def get_fixture_path(filename):
    p = join(dirname(__file__), 'fixtures', filename)
    return abspath(p)
