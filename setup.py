from setuptools import setup, find_packages
from pathlib import Path
import sys
import os


long_description = None
this_directory = Path(__file__).parent.absolute()

try:
    with open(this_directory.joinpath('README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
except IOError:
    long_description = 'See https://github.com/Aurococcus/wasd'


if sys.argv[-1] == 'publish':
    print("\n*** Cleanup dist: ***")
    os.system('rm -rf dist/ build/')

    print("\n*** Creating new tar/wheel: ***\n")
    os.system('python setup.py sdist bdist_wheel')
    
    try:
        import twine
        print('\n*** twine OK ***\n')
    except ImportError:
        print('\n*** Installing twine: ***\n')
        os.system('python -m pip install twine')

    print("\n*** Publishing to PyPI: ***\n")
    os.system('python -m twine upload dist/*')  # Requires ~/.pypirc Keys

    print("\n*** Release published successfully. ***\n")

    sys.exit()


setup(
    name='wasd',
    version='1.0.92',
    description='The Kostyan Selenium Wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Aurococcus/wasd',
    author='Kostyan Opasnost',
    author_email='aurococcus@gmail.com',
    maintainer='Kostyan',
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'pip>=20.0.2',
        'setuptools',
        'wheel',
        'pytest>=5.3.5;python_version>="3"',
        'selenium>=3.141.0',
        'lxml',
        'cssselect',
        'pyyaml',
        'invoke',
        'colorlog',
        'pyhamcrest',
        'termcolor'
    ],
    include_package_data = True,
    entry_points={
        'console_scripts': [
            "wasd = wasd.cli.scaffold:main"
        ],
        'pytest11': ['wasd.fixtures = wasd.core.fixtures']
    }
)
