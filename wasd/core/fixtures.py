import pytest
from pathlib import Path
from wasd.core import SettingsManager
from wasd.core import session
from termcolor import colored
from wasd.common.logger import LOGGER, __fake_logger
from wasd.wd import Browser
import uuid
import os


if not os.path.exists(Path.cwd().joinpath('_wasd_settings.yml')):
    '''
    Do not load plugin if there is no `_wasd_settings.yml` file
    '''
    pass

else:
    def pytest_addoption(parser):
        parser.addoption("--env", action="store")
        parser.addoption("--listener", action="store_const", const=False)
        parser.addoption("--save-screenshot", action="store_const", const=False)
        parser.addoption("--steps", action="store_const", const=False)

    def pytest_configure(config):
        config.addinivalue_line("markers", "want_to(arg): hello world.")

    @pytest.fixture(scope='session', autouse=True)
    def init_settings_fixture(request):
        session.env = request.config.getoption("--env")
        session.use_listener = True if request.config.getoption("--listener") is not None else False
        session.save_screenshot = True if request.config.getoption("--save-screenshot") is not None else False
        session.steps = True if request.config.getoption("--steps") is not None else False
        SettingsManager.init(session.env)

    def pytest_runtest_logfinish(nodeid, location):
        print()

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(item):
        __fake_logger.log(61, "\n" + item.pretty_id)
        if session.steps:
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

    @pytest.mark.hookwrapper
    def pytest_runtest_makereport(item, call):
        outcome = yield
        report = outcome.get_result()

        browser = item.funcargs.get("browser")
        if browser and isinstance(browser, Browser):
            driver = browser._driver_instance
            item.browser = browser

            if report.failed:
                if driver is None:  # If driver was closed
                    return
                item.screenshot_path, item.screenshot_binary = take_screenshot(driver, item)

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


def load():
    """Required for `pluggy` to load a plugin from setuptools entrypoints."""
