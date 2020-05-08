import os
import sys
from pathlib import Path
from termcolor import cprint


def show_usage():
    print('Type "wasd scaffold" for generate project stucture at current directory')
    print('* (Use "pytest" for running tests) *\n')


def main():
    num_args = len(sys.argv)

    if num_args != 2 or sys.argv[1] != 'scaffold':
        show_usage()
        return

    proj_dir = Path.cwd()

    if os.path.exists(proj_dir.joinpath('_wasd_settings.yml')):
        cprint(f'Project under "{proj_dir}" already exists', 'red')
        return

    test_dir = proj_dir.joinpath('tests')
    output_dir = proj_dir.joinpath('_output')
    os.mkdir(test_dir)
    os.mkdir(output_dir)
    os.mkdir(proj_dir.joinpath('_data'))
    

    this_directory = Path(__file__).parent.absolute()

    # source : dist
    files_to_create = [
        ('config_browsers.json.txt',    ['config', 'browsers.json']),
        ('tests_conftest.py.txt',   ['tests', 'conftest.py']),
        ('tests_sample.py.txt',     ['tests', 'test_something.py']),
        ('env_stable.yml.txt',      ['_env', 'stable.yml']),
        ('_wasd_settings.yml.txt',   ['_wasd_settings.yml']),
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
        dist_path = proj_dir.joinpath(*dist)
        dist_path.parent.mkdir(parents=True, exist_ok=True)

        with open(source_path, 'r') as sf:
            sd = sf.read()
            with open(dist_path, 'w+') as df:
                cprint(f"> {dist_path}", 'cyan')
                df.write(sd)
    cprint('  --- ', 'cyan')
