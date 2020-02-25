import logging
import colorlog
import shutil
from contextlib import contextmanager

STEP = 60

formatter = colorlog.ColoredFormatter(
    "\n%(log_color)s[%(levelname)8s] %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL':	'bold_red,bg_white',
        'STEP':		'bold_green'
    },
    secondary_log_colors={},
    style='%'
    )

logging.addLevelName(STEP, 'STEP')

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)

LOGGER = colorlog.getLogger(__name__)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)


@contextmanager
def _step(message, limit = None):
    term_width = shutil.get_terminal_size().columns
    
    msg = message[:limit] if limit else message[:term_width * 3]
    if len(msg) < len(message):
        msg += " ..."

    LOGGER.log(STEP, msg)
    yield
