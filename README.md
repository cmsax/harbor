# Harbor

A package to crawl, backup and export weibo content.

## Installation

### Requirements

- Python 3.7 and up

## Usage

Install and run binary via python setup-tools.

```
$ python3 -m venv env
$ python3 -m pip install -r requirements.txt
$ python3 setup.py install
$ env/bin/harbor
```

## Development

```
$ python3 -m venv env
$ . env/bin/activate
$ pip install -e .
```

Once you update requirements, make sure use `pip-compile` to refresh `requirements.txt`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
