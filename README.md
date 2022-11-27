# multi-echelon-scn

## Development

### Setup project

* Create/copy config file:
```sh
cp config_example.json config.json
```

* Change config settings if needed

* Create venv
```sh
python3 -m venv ./venv
```

* Activate venv
```sh
. ./venv/bin/activate
```


* Install libs
```sh
pip install -r ./requirements/dev.txt
```

* Run program
```py
python3 ./src/main.py
```

### Test code

* Linter (flake8)
```sh
flake8 ./src/
```

* Unit tests (pytest)
```sh
cd ./src/
python -m pytest tests/
```


### Instance format example

TODO
