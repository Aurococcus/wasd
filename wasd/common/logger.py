import logging
import colorlog
import shutil
from contextlib import contextmanager
import inspect


STEP = 60

formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname)8s] %(message)s",
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



def __log_substep(message, indent=4, limit=None):
    LOGGER.debug( _prep_msg(message, indent, limit))


def __log_step(message, indent=0, limit=None):
    LOGGER.log(STEP, _prep_msg(message, indent, limit))


__c_frame = 0 # curr
__p_frame = 0 # prev


def log_step(message, indent=0, limit=None):
    global __c_frame, __p_frame


    lvl = 0
    while inspect.stack()[lvl].function not in ['pytest_pyfunc_call', 'call_fixture_func']:
        lvl += 1
    lvl -= 2


    __c_frame = id(inspect.stack()[lvl].frame)
    if lvl == 1:
        __log_step(message)
    else:
        if __c_frame != __p_frame:
            human_str = ' '.join([ i.capitalize() for i in inspect.stack()[lvl].function.split('_') ])
            frame = inspect.stack()[lvl].frame
            args, _, _, values = inspect.getargvalues(frame)
            argspec = ', '.join([ f"'{values[i]}'" for i in args[1:] ])
            __log_step(human_str + " " + argspec)
        __log_substep(message)

    __p_frame = __c_frame


def _prep_msg(message, indent, limit):
    term_width = shutil.get_terminal_size().columns
    
    msg = message[:limit] if limit else message[:term_width * 3]
    if len(msg) < len(message):
        msg += " ..."
    return ' ' * indent + msg
