# pychain
Pychain is an implementation of NaiveChain in Python3

# Getting Started

Download pytest on your local directory.
```
git clone https://github.com/naoto67/pychain.git
```

Install dependencies.
```
cd <project dir>
pip install -r requirements.txt
```

# Test

Test pychain code on your enviroment
```
pytest -v --flake8 --pep8
```

# How to run pychain server in development enviroment

Run server on 8000 port as default

```
python main.py
```

Get blocks via curl command
```
curl http://localhost:8000/blocks
```

Add blocks via curl command
```
curl --data '{"data" : "Some data to the first block"}' http://localhost:8000/mineBlock
```

# License

MIT license
