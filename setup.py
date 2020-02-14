from setuptools import setup, find_packages


setup(
    name='wasd',
    version='1.0.1',
    description='The Kostyan Selenium Wrapper',
    url='https://example.com',
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
        'pyhamcrest'
    ],
    entry_points={
        'console_scripts': [
            "wasd = wasd.cli.scaffold:main"
        ],
        'pytest11': ['wasd.fixtures = wasd.core.fixtures']
    }
)
