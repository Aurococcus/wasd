import pytest
from wasd.core import SettingsManager
from wasd.core import session


def pytest_addoption(parser):
    parser.addoption("--env", action="store")
    parser.addoption("--listener", action="store_const", const=False)


@pytest.fixture(scope='session', autouse=True)
def init_settings_fixture(request):
    session.env = request.config.getoption("--env")
    session.use_listener = True if request.config.getoption("--listener") is not None else False
    SettingsManager.init(session.env)
