import logging
import colorlog
import shutil
from contextlib import contextmanager
import inspect
from termcolor import colored, cprint
from wasd.core import session


STEP = 60

formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname).1s] %(message)s",
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

#
#
#

__fake_formatter = colorlog.ColoredFormatter(
    "%(message)s",
    reset=True,
    style='%'
)

logging.addLevelName(1001, 'PRINT')
__fake_handler = colorlog.StreamHandler()
__fake_handler.setFormatter(__fake_formatter)

__fake_logger = colorlog.getLogger('PRINT')
__fake_logger.addHandler(__fake_handler)
__fake_logger.setLevel(logging.DEBUG)


def __log_substep(message, limit=None):
    global __fake_logger
    text = colored(_prep_msg(message, 4, limit), 'cyan')
    __fake_logger.log(61, text)


def __log_step(message, limit=None):
    global __fake_logger
    text = colored(_prep_msg(message, 2, limit), 'green', attrs=['bold'])
    __fake_logger.log(61, text)


__c_frame = 0
__p_frame = 0
__c_lvl = 0
__p_lvl = 0


def log_step(message, limit=None):
    if not session.steps:
        return
    global __c_frame, __p_frame, __c_lvl, __p_lvl

    lvl = 0
    while inspect.stack()[lvl].function != "browser":
        if inspect.stack()[lvl].function in ["pytest_pyfunc_call", "_multicall"]:
            lvl -= 1
            break

        lvl += 1

    lvl -= 1
    __c_lvl = inspect.stack()[lvl+1].frame.f_lineno
    __c_frame = id(inspect.stack()[lvl].frame)

    if lvl == 1:
        __log_step(message)
    else:
        human_str = ' '.join([i.capitalize() for i in inspect.stack()[lvl].function.strip('_').split('_')])
        frame = inspect.stack()[lvl].frame
        args, _, _, values = inspect.getargvalues(frame)
        argspec = ', '.join([f"'{values[i]}'" for i in args[1:]])
        if __c_frame != __p_frame:
            __log_step(human_str + " " + argspec)
        else:
            if __c_lvl != __p_lvl:
                __log_step(human_str + " " + argspec)

        __log_substep(message)

    __p_frame = __c_frame
    __p_lvl = __c_lvl


def _prep_msg(message, indent, limit):
    term_width = shutil.get_terminal_size().columns

    msg = message[:limit] if limit else message[:term_width * 3]
    if len(msg) < len(message):
        msg += " ..."
    return ' ' * indent + msg
