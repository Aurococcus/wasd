import os
import sys
from pathlib import Path
from termcolor import cprint


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

    new_dir = Path(os.getcwd(), dir_name)
    if os.path.exists(new_dir):
        raise Exception(f'Directory "{new_dir}" already exists')

    test_dir = new_dir.joinpath('tests')
    os.mkdir(new_dir)
    os.mkdir(test_dir)
    

    this_directory = Path(__file__).parent.absolute()

    # source : dist
    files_to_create = [
        ('config_browsers.json.txt',    ['config', 'browsers.json']),
        ('tests_conftest.py.txt',   ['tests', 'conftest.py']),
        ('tests_sample.py.txt',     ['tests', 'test_something.py']),
        ('env_stable.yml.txt',      ['_env', 'stable.yml']),
        ('_settings.yml.txt',   ['_settings.yml']),
        ('base_page.py.txt',    ['page', 'base_page.py']),
        ('home_page.py.txt',    ['page', 'home_page.py']),
        ('requirements.txt',    ['requirements.txt']),
        ('__init__.py.txt', ['tests', '__init__.py']),
        ('__init__.py.txt', ['page', '__init__.py']),
        ('pytest.ini.txt',  ['pytest.ini']),
        ('tasks.py.txt',    ['tasks.py'])
    ]

    for source, dist in files_to_create:
        source_path = this_directory.joinpath('boilerplate', source)
        dist_path = new_dir.joinpath(*dist)
        dist_path.parent.mkdir(parents=True, exist_ok=True)

        with open(source_path, 'r') as sf:
            sd = sf.read()
            with open(dist_path, 'w+') as df:
                cprint(f"> {dist_path}", 'cyan')
                df.write(sd)
    cprint('  --- ', 'cyan')
