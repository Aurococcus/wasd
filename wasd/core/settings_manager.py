import yaml
import re
import os
from wasd.core import session
from wasd.common import LOGGER


class SettingsManager:

    _default_config_file = session.root_dir.joinpath('_wasd_settings.yml')

    _default_config = {
        'protocol': 'http',
        'host':     'localhost',
        'port':     '4444',
        'path':     '/wd/hub',
        'implicit_timeout': 5,
        'window_size':      '800x600'
    }

    @classmethod
    def init(cls, env):
        cls._load_env_file(env)
        cls._parse_window_size()

    @classmethod
    def _load_env_file(cls, env=None):
        if env is not None:
            env_file = session.env_dir.joinpath(f'{env}.yml')
        else:
            env_file = cls._default_config_file

        try:
            with open(env_file, 'r') as f:
                data = f.read()
        except IOError:
            LOGGER.error(f"Env file '{env_file}' not found.")
            raise

        cls._config = {
            **cls._default_config,
            **cls._prepare_config(yaml.safe_load(data))
        }

    @classmethod
    def get(cls, k):
        return cls._config[k]

    @classmethod
    def _prepare_config(cls, d):
        for k, v in d.items():
            if isinstance(v, dict):
                cls._prepare_config(v)
            else:
                if isinstance(v, list):
                    for i, _ in enumerate(v, start=0):
                        if isinstance(_, str):
                            d[k][i] = re.sub(
                                r'%(\w+)%',
                                lambda match: os.environ[match.group(1)], v[i]
                            )
                else:
                    if isinstance(v, str):
                        d[k] = re.sub(
                            r'%(\w+)%',
                            lambda match: os.environ[match.group(1)], v
                        )
        return d

    @classmethod
    def _parse_window_size(cls):
        raw_data = cls.get('window_size')
        if raw_data == 'maximize':
            return
        parsed = tuple(list(map(lambda v: int(v), raw_data.split('x'))))
        cls._config['window_size'] = parsed
