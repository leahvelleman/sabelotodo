# sabelotodo

## Installation

Clone the repository. 
```

```
Inside the new directory, set up and activate a virtual environment.
```
cd sabelotodo
python -m venv --prompt sabelotodo env
source env/bin/activate
```
Then, install the project dependencies inside it.
```
pip install -r requirements.txt
```

## Use

Set up `hello.py` as the default Flask app.
```
export FLASK_APP=hello.py
```
Then, run Flask.
```
flask run
```
In a web browser, load the URL `http://127.0.0.1:5000/`. A page with "Hello, world!" appears.
