# sabelotodo

## Prerequisites

For installation, this package requires Python 3.8, a current version of Pip, and an internet connection. The installation commands
will download the remaining dependencies, which include Flask 1.1.1.

## Installation

Clone the repository. 
```
git clone https://github.com/leahvelleman/sabelotodo/
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

## Usage

Set up `hello.py` as the default Flask app.
```
export FLASK_APP=hello.py
```
Then, run Flask.
```
flask run
```
In a web browser, load the URL `http://127.0.0.1:5000/`. A page with "Hello, world!" appears.

## Contributing

To install new dependencies, use `pip` as you would normally. Then, update the requirements file.
```
pip freeze > requirements.txt
```
To deactivate the virtual environment and resume using your default system Python, use the command `deactivate`. To reactivate it, use `source env/bin/activate`.
