import pytest
from wasd.core import SettingsManager
from wasd.core import session
from termcolor import colored, cprint


def pytest_addoption(parser):
    parser.addoption("--env", action="store")
    parser.addoption("--listener", action="store_const", const=False)


@pytest.fixture(scope='session', autouse=True)
def init_settings_fixture(request):
    session.env = request.config.getoption("--env")
    session.use_listener = True if request.config.getoption("--listener") is not None else False
    SettingsManager.init(session.env)


def pytest_runtest_logstart(nodeid, location):
    cprint('\nScenario --', 'yellow')


def pytest_itemcollected(item):
    test_id = item._nodeid

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

    pretty_id += "\n\r{0}: {1}".format(
        colored('Test', 'green'),
        colored(test_id, 'white')
    )
    item._nodeid = pretty_id
