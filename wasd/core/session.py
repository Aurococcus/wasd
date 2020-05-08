from pathlib import Path
import os


root_dir = Path(os.getcwd())
test_dir = root_dir.joinpath('tests')
env_dir = root_dir.joinpath('_env')
output_dir = root_dir.joinpath('_output')
data_dir = root_dir.joinpath('_data')

env = None
use_listener = None
save_screenshot = None
steps = None