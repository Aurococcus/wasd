import pytest
from wasd.core import SettingsManager
from wasd.core import session
from termcolor import colored, cprint
from wasd.common.logger import __fake_logger


def pytest_addoption(parser):
    parser.addoption("--env", action="store")
    parser.addoption("--listener", action="store_const", const=False)


@pytest.fixture(scope='session', autouse=True)
def init_settings_fixture(request):
    session.env = request.config.getoption("--env")
    session.use_listener = True if request.config.getoption("--listener") is not None else False
    SettingsManager.init(session.env)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    __fake_logger.log(61, "\n" + item.pretty_id)
    __fake_logger.log(61, colored('Scenario --', 'yellow'))


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        pretty_id = colored(item.parent.parent.name + ": ", 'magenta', attrs=['bold'])
    
        # Если будет несколько маркеров, то просто брать последний, не кидая ошибку
        want_to_list = list(filter(lambda m: m.name == 'want_to', item.own_markers))
        if len(want_to_list) >= 1:
            func_id = want_to_list[-1].args[0]
        else:
            splitted = item.name.split('_')
            captalized = splitted[0].capitalize() + ' ' + ' '.join(splitted[1:])
            func_id = captalized

        pretty_id += colored(func_id, 'white', attrs=['bold'])

        item.pretty_id = pretty_id
