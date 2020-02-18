# Yet another selenium wd wrapper

## Requirements

* python >= 3.6
* pyenv is recommended ([pyenv](https://github.com/pyenv/pyenv) & [pyenv virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv))
* Docker with pulled image `selenoid/vnc_chrome:##.#` (https://hub.docker.com/r/selenoid/vnc_chrome)

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
wasd scaffold hello_world
cd hello_world
invoke selenoid.up
pytest tests
```

Then go to `localhost:8080`


## Api

```
new_driver(self)
get_driver(self)
close_driver(self)
open(self, path)
open_url(self, url)
refresh(self)
grab_page_html(self)
grab_html_from(self, element)
clear_field(self, input_element)
fill_field(self, element, text)
fill_field_with_delay(self, element, text, delay = 0.1)
press_key(self, element, *chars)
append_field(self, element, text)
wait_for_element_visible(self, element, timeout = 5)
wait_for_element_not_visible(self, element, timeout = 5)
see_element(self, element, attributes = {})
see_text(self, text, element = None)
see_in_field(self, input_element, needle)
grab_visible_text(self, element = None)
click(self, element)
grab_visible(self, element)
grab_text_from(self, element)
grab_attribute_from(self, element, attribute)
grab_value_from(self, input_element)
grab_multiple(self, elements)
move_mouse_over(self, element)
switch_to_iframe(self, frame = None)
save_session_snapshot(self, name)
load_session_snapshot(self, name)
set_cookie(self, name, value, params = {})
scroll_to(self, element, offset_x = 0, offset_y = 0)
scroll_into_view(self, element, offset_x = 0, offset_y = 0)
delete_all_cookies(self)
execute_js(self, script, *args)
sleep(self, secs)
wd_wait(self, timeout = 10, poll_frequency = 0.5)
scroll_top(self)
find(self, element)
finds(self, element)
```