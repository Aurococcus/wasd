import logging
import colorlog


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

logging.addLevelName(60, 'STEP')

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)

LOGGER = colorlog.getLogger(__name__)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)
