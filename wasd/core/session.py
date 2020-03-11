from pathlib import Path
import os


root_dir = Path(os.getcwd())
test_dir = root_dir.joinpath('tests')
env_dir = root_dir.joinpath('_env')
output_dir = root_dir.joinpath('_output')

env = None
use_listener = None
save_screenshot = None
