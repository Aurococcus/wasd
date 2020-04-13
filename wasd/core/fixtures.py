import pytest
from pathlib import Path
from wasd.core import SettingsManager
from wasd.core import session
from termcolor import colored
from wasd.common.logger import LOGGER, __fake_logger
from wasd.wd import Browser
import uuid
import os


def pytest_addoption(parser):
    parser.addoption("--env", action="store")
    parser.addoption("--listener", action="store_const", const=False)
    parser.addoption("--save-screenshot", action="store_const", const=False)


@pytest.fixture(scope='session', autouse=True)
def init_settings_fixture(request):
    session.env = request.config.getoption("--env")
    session.use_listener = True if request.config.getoption("--listener") is not None else False
    session.save_screenshot = True if request.config.getoption("--save-screenshot") is not None else False
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


@pytest.fixture(scope='function')
def browser(request, _browser):
    yield _browser


@pytest.fixture(scope='function', autouse=True)
def set_driver_to_test(request, browser):
    request.node.obj.__func__.browser = browser


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        test_func = item.obj
        if hasattr(test_func, 'browser'):
            item.screenshot_path, item.screenshot_binary = take_screenshot(test_func.browser._driver_instance, item)


def take_screenshot(driver, item):
    id_ = f"{item.location[2]}__{uuid.uuid4()}.png"
    screenshot_path = str(session.output_dir.joinpath(id_))

    if session.save_screenshot:
        if not os.path.exists(session.output_dir):
            os.mkdir(session.output_dir)
        driver.get_screenshot_as_file(screenshot_path)
        __fake_logger.log(61, colored(f'◉ Screenshot saved to: {screenshot_path}', 'green'))

    screenshot_binary = driver.get_screenshot_as_png()
    return (screenshot_path, screenshot_binary)
