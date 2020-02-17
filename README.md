# Yet another selenium wd wrapper

## Requirements

* python >= 3.6
* pyenv is recommended ([pyenv](https://github.com/pyenv/pyenv) & [pyenv virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv))
* Docker with pulled image `selenoid/vnc_chrome:##:#` (https://hub.docker.com/r/selenoid/vnc_chrome)

## Install

```sh
$ git clone git@github.com:Aurococcus/wasd.git
cd wasd
pip install .
```

## Run

```sh
wasd scaffold hello_world
cd hello_world
invoke selenoid.up
pytest tests
```

Then go to `localhost:8080`
