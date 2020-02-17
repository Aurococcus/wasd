import os
import sys


def show_usage():
    print('Type "wasd scaffold" for generate default config, '
          'directory stucture and sample test.')
    print('* (Use "pytest" for running tests) *\n')


def main():
    num_args = len(sys.argv)
    if num_args <= 2 or num_args > 3:
        show_usage()
        return

    dir_name = sys.argv[-1]

    if os.path.exists(os.getcwd() + '/' + dir_name):
        raise Exception(f'Directory "{dir_name}" already exists')

    env_dir = f"{dir_name}/_env"
    test_dir = f"{dir_name}/tests"

    os.mkdir(dir_name)
    os.mkdir(test_dir)
    os.mkdir(env_dir)
    os.mkdir(f"{dir_name}/config")

    #
    # pytest.ini
    #
    data = []
    data.append("[pytest]")
    data.append("addopts = -sv --color=yes")
    data.append("log_cli_level = INFO")
    data.append("log_cli_format = [%(levelname)8s] %(message)s")
    data.append("markers =")
    data.append("    allure_description")
    data.append("    allure_title")
    data.append("")

    file_path = f'{dir_name}/pytest.ini'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    #
    # conftest
    #
    data = []
    data.append("import pytest")
    data.append("from wasd.wd import Browser")
    data.append("\n"*2)
    data.append("# Define custom action here")
    data.append("class MyExtendedBrowser(Browser):")
    data.append("   def __init__(self):")
    data.append("       super().__init__()")
    data.append("")
    data.append("   def my_super_fn(self):")
    data.append("       print('Hello')")
    data.append("\n")
    data.append("@pytest.fixture(scope='class')")
    data.append("def browser():")
    data.append("   b = MyExtendedBrowser()")
    data.append("   yield b")
    data.append("   b.close_driver()")
    data.append("")

    file_path = f'{dir_name}/tests/conftest.py'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    #
    # test file
    #
    data = []
    data.append("from wasd.wd import Element as E")
    data.append("import time")
    data.append("\n")
    data.append("class TestSomething:")
    data.append("")
    data.append("    def test_feature1(self, browser):")
    data.append("        browser.open_url('https://google.com')")
    data.append("        browser.fill_field( E(\"[name = 'q']\"), 'Hello, World!' )")
    data.append("        time.sleep(5)")
    data.append("")

    file_path = f'{test_dir}/test_something.py'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    #
    # TODO: page
    #
    # data = []
    # data.append('from page.base_page import BasePage')
    # data.append('from web_driver.find import Find')
    # data.append("\n"*3)
    # data.append('class HomePage(BasePage):')
    # data.append('\n')
    # data.append('    URL = /home')
    # data.append('\n')
    # data.append('    def __init__(self, browser):')
    # data.append('        self.browser = browser')
    # data.append('\n')
    # data.append('    def navigate(self):')
    # data.append('        self.browser.open(self.URL)')
    # data.append('        self.validate()')
    # data.append('        return self')
    # data.append('\n')
    # data.append('    def validate(self):')
    # data.append('        return self')
    # data.append("")

    #
    # _env & settings
    #
    data = []
    data.append("# web driver")
    data.append("url: 'http://example.ru'")
    data.append("implicit_timeout: 5")
    data.append("window_size: 'maximize'")
    data.append("")
    data.append("# grid / selenoid")
    data.append("protocol: 'http'")
    data.append("host:     'localhost'")
    data.append("port:     '4444'")
    data.append("path:     '/wd/hub'")
    data.append("")
    data.append("# data")
    data.append("username: 'admin'")
    data.append("password: 'admin'")
    data.append("")
    data.append("# caps")
    data.append("capabilities:")
    data.append("    browserName: 'chrome'")
    data.append("    unexpectedAlertBehaviour: 'accept'")
    data.append("    enableVNC: True")
    data.append("    screenResolution: '1920x1080x24'")
    data.append("    loggingPrefs:")
    data.append("        browser: 'INFO'")
    data.append("    chromeOptions:")
    data.append("        args: ['--disable-infobars']")
    data.append("")

    file_path = f'{env_dir}/stable.yml'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    file_path = f'{dir_name}/_settings.yml'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    #
    # tasks
    #
    data = []
    data.append("from invoke import Collection, task")
    data.append("")
    data.append("@task")
    data.append("def selenoid_up(c):")
    data.append("    selenod='''docker run -d --rm               \\")
    data.append("--name selenoid                                 \\")
    data.append("-p 4444:4444                                    \\")
    data.append("-v /var/run/docker.sock:/var/run/docker.sock    \\")
    data.append("-v `pwd`/config/:/etc/selenoid/:ro              \\")
    data.append("-v `pwd`/video/:/opt/selenoid/video/            \\")
    data.append("-e OVERRIDE_VIDEO_OUTPUT_DIR=`pwd`/video/       \\")
    data.append("-e TZ=Asia/Novosibirsk                          \\")
    data.append("aerokube/selenoid:latest-release -limit 10'''")
    data.append("    c.run(selenod)")
    data.append("\n")
    data.append("    selenod_ui='''docker run -d --rm    \\")
    data.append("--name selenoid-ui                      \\")
    data.append("--link selenoid                         \\")
    data.append("-p 8080:8080                            \\")
    data.append("aerokube/selenoid-ui --selenoid-uri=http://selenoid:4444'''")
    data.append("    c.run(selenod_ui)")
    data.append("\n")
    data.append("@task")
    data.append("def selenoid_down(c):")
    data.append("    c.run('docker stop selenoid')")
    data.append("    c.run('docker stop selenoid-ui')")
    data.append("")
    data.append("ns = Collection()")
    data.append("selenoid = Collection('selenoid')")
    data.append("selenoid.add_task(selenoid_up, 'up')")
    data.append("selenoid.add_task(selenoid_down, 'down')")
    data.append("ns.add_collection(selenoid)")
    data.append("")

    file_path = f'{dir_name}/tasks.py'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    #
    # selenoid config
    #
    data = []
    data.append('{')
    data.append('    "chrome": {')
    data.append('        "default": "74.0",')
    data.append('        "versions": {')
    data.append('            "74.0": {')
    data.append('                "image": "selenoid/vnc_chrome:74.0",')
    data.append('                "port": "4444",')
    data.append('                "path": "/",')
    data.append('                "env" : ["TZ=Asia/Novosibirsk", "ENABLE_WINDOW_MANAGER=1"]')
    data.append('            }')
    data.append('        }')
    data.append('    }')
    data.append('}')
    data.append("")
        
    file_path = f'{dir_name}/config/browsers.json'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))

    #
    # requirements.txt
    #
    data = []
    data.append('wasd')
    data.append('')

    file_path = f'{dir_name}/requirements.txt'
    with open(file_path, 'w+') as f:
        f.writelines("\n".join(data))
    