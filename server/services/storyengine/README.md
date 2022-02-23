Where ENV is a directory in which to place the new virtual environment.

```
virtualenv ENV
```
Activate virtual environment

```
source ./ENV/bin/activate
```

install requirements with Python 3
```
pip install -r requirements.txt 
```

Start Test Application Server on localhost:5000

```
cd server
python run.py 
```

Run Application Server on Real Environment with Gunicorn

```
gunicorn -c gunicorn.py run:app
```

Deactivate virtual environment

```
deactivate
```

Dockerise

```
docker build -t calliope/story-engine .
```