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
pytest -v --flack5 --pep8
```

# curlの使い方
Get
```
curl http://localhost:8000/hello?name=<name>
```

Post
```
curl --data 'name=<name>' http://localhost:8000/hellopost
```

# License

MIT license
