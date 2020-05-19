# Yet another selenium wd wrapper

## Requirements

* python >= 3.6
* pyenv is recommended ([pyenv](https://github.com/pyenv/pyenv) & [pyenv virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv))
* Docker & image `selenoid/vnc_chrome:##.#` (https://hub.docker.com/r/selenoid/vnc_chrome)

## Install

Build from source:
```sh
$ git clone git@github.com:Aurococcus/wasd.git
$ cd wasd
$ pip install .
```

From pypi:
```sh
$ pip install wasd
```

## Run

```sh
$ mkdir hello_world
$ cd hello_world
# activate vevn e.g. $ pyenv local my_venv
$ pip install wasd
$ wasd scaffold
$ invoke selenoid.up
$ pytest tests
```

Then go to `localhost:8080`

## CLI options

- `$ pytest --env=<env>` - run tests with settings `<env>.yml` from `_env` dir
- `$ pytest --listener` - highlight found element during runtime
- `$ pytest --save-screenshot` - save screenshot on failure in `_output` dir
- `$ pytest --steps` - enable verbose log


## Api

```
def new_driver(self)
def get_driver(self)
def close_driver(self)
def open(self, path)
def open_url(self, url)
def refresh(self)
def grab_console_log(self)
def grab_page_html(self)
def grab_html_from(self, element)
def clear_field(self, input_element)
def fill_field(self, element, text)
def fill_field_with_delay(self, element, text, delay = 0.1)
def press_key(self, element, *chars)
def append_field(self, element, text)
def wait_for_element_visible(self, element, timeout = 5)
def wait_for_element_not_visible(self, element, timeout = 5)
def see_element(self, element, attributes = {})
def see_text(self, text, element = None)
def see_in_field(self, input_element, needle)
def see_number_of_elements(self, element, expected)
def click(self, element)
def grab_visible(self, element)
def grab_text_from(self, element)
def grab_attribute_from(self, element, attribute)
def grab_value_from(self, input_element)
def grab_multiple(self, elements)
def save_screenshot(self, name=None)
def get_screenshot_binary(self)
def move_mouse_over(self, element)
def switch_to_iframe(self, frame = None)
def save_session_snapshot(self, name)
def load_session_snapshot(self, name)
def set_cookie(self, name, value, params = {})
def scroll_to(self, element, offset_x = 0, offset_y = 0)
def scroll_into_view(self, element, offset_x = 0, offset_y = 0)
def delete_all_cookies(self)
def element_has_attribute(self, element, attr, expected_value = None)
def execute_js(self, script, *args)
def sleep(self, secs)
def wd_wait(self, timeout = 10, poll_frequency = 0.5)
def scroll_top(self)
def find(self, element)
def finds(self, element)
```