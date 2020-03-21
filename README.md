# sabelotodo

## Prerequisites

For installation, the backend requires Python 3.8, a current version of Pip, Postgresql, and an internet connection. 
The installation commands will download the remaining dependencies, which include Flask 1.1.1 and SQLAlchemy 1.3.15.

Currently, the Postgresql database name is hardwired as `sabelotodo_dev`.

The frontend requires npm; the installation commands will download the remaining dependencies.

### For mac users
Install fsevents: `npm install fsevents`

## Installation

### File setup

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
npm install
```

### Autoenv setup

The autoenv tool manages environment variables for the project and
automatically activates the virtual environment when you enter the project
directory. Install it *outside* the virtual environment.

```
deactivate
pip install autoenv==1.0.0
```

Then, add ``source `which activate.sh` `` to your .bashrc or other startup
file, and rerun that file. Now, when you leave and reenter the directory, the
virtual environment activates automatically. 

### Database setup

The database is managed by Alembic. To create it for the first time, first
enter the project directory to activate the virtual environment. Then, initialize
the migrations directory, set up a migration, and upgrade to it.
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
The database is created at `sabelotodo_dev`, and contains a table of Alembic
information and the table that will store to-do items for the application.
```
~> psql sabelotodo_dev
psql (12.2)
Type "help" for help.

sabelotodo_dev=# \dt
                List of relations
 Schema |      Name       | Type  |    Owner
--------+-----------------+-------+--------------
 public | alembic_version | table | leahvelleman
 public | items           | table | leahvelleman
(2 rows)
```


## Usage

Run `npm run start` to build the react app and start the Flask server (in development mode).

In a web browser, load the URL `http://127.0.0.1:3000/`. A page with a default React app appears.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm run start-prod`

Builds the app for production and runs the app in production mode. Open [http://localhost:5000](http://localhost:5000) to view it in the browser.<br />
The page will not automatically reload when you make edits.

### `npm test`

Launches the frontend test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

## Contributing

To install new dependencies, use `pip` as you would normally. Then, update the requirements file.
```
pip freeze > requirements.txt
```
To deactivate the virtual environment and resume using your default system Python, use the command `deactivate`. To reactivate it, use `source env/bin/activate`.
