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


### Instance (format) example
*File: "./instances/example1.yaml"*

```yaml
D: 2    # number of suppliers
F: 3    # number of factories
M: 3    # number of warehouses
S: 5    # number of shops

sd: [13, 27]                # MAX production capacity of suppliers (związane z xdminmax [SUMA])
sf: [17, 14, 16]            # MAX production capacity of factories (związane z xfminmax [SUMA])
sm: [50, 40, 60]            # MAX capacity of warehouses (związane z xmminmax [SUMA])
ss: [60, 45, 50, 70, 50]    # MAX market demand (we can also call this capacity)

# cost of "suppliers -> factories" e.g.: D1 -> F1 (3),  D1 -> F2 (7), D2 -> F2 (1)
cd: [3, 7, 2, 4, 1, 5]
cf: [8, 3, 7, 4, 1, 9, 3, 8, 4]                     # cost of "factories -> warehouses"
cm: [9, 3, 7, 5, 1, 4, 7, 9, 3, 5, 1, 4, 3, 7, 5]   # cost of "warehouses -> shops"

ud: [80, 60]        # one-time cost of enabling supplier
uf: [70, 40, 90]    # one-time cost of enabling factory
um: [90, 34, 58]    # one-time cost of enabling warehouse

p: [800, 500, 700, 500, 600]    # shop income (per product)

xdminmax: [1, 9, 4, 9, 3, 7, 4, 9, 3, 7, 7, 9]                      # "suppliers -> factories" min-max transport
xfminmax: [2, 9, 3, 8, 4, 5, 3, 9, 2, 8, 4, 9, 2, 8, 3, 7, 2, 8]    # "factories -> warehouses min-max transport
xmminmax: [3, 8, 2, 7, 3, 9, 4, 8, 2, 7, 3,
           9, 1, 6, 3, 9, 2, 8, 3, 7, 1, 8,
           2, 8, 3, 7, 1, 8, 3, 7]                                  # "warehouses -> shops" min-max transport

```
