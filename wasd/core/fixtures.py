import pytest
from wasd.core import SettingsManager


def pytest_addoption(parser):
    parser.addoption("--env", action="store")


@pytest.fixture(scope='session', autouse=True)
def init_settings_fixture(request):
    env = request.config.getoption("--env")
    SettingsManager.init(env)
