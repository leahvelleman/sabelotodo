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
pip install -r requirements-dev.txt
npm install
```

### Environment variables

On macOS, create a file in the root directory called `.env` with the following lines, filling in your username
and password. The project `.gitignore` keeps this file from being pushed to the server, so it is a relatively
safe place for a password. Omit `DB_PASSWORD` if the database is not password-protected.
```
export SQLALCHEMY_DATABASE_URI="postgresql:///sabelotodo_dev"
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=<your postgres username>
export DB_DATABASE=sabelotodo_test
export DB_PASSWORD=<your db password>
export TEST_DATABASE_URL=postgresql:///sabelotodo_test
```
On Linux, do not set the `DB_HOST` and `DB_PORT` environment variables. Create
a superuser as the `DB_USER` which matches the username of the user that runs
the tests.

To set up the environment variables before running or testing the project, use `source .env`.

### Using Autoenv

Alternatively, you can execute your `.env` file using a tool called Autoenv.
The Autoenv tool manages environment variables for the project and
automatically activates the virtual environment when you enter the project
directory. It is optional but convenient.

To use it, install it *outside* the virtual environment.
```
deactivate
pip install autoenv==1.0.0
```
Then, add the `export` commands above to a file called `.env`.  Finally, add
``source `which activate.sh` `` to your `.bashrc` or other startup file, and
rerun that file. Now, when you leave and reenter the project directory, the
virtual environment activates automatically. 

If you do not use Autoenv, 

### Database setup

The first time you install the project, you must create a database for it.
```
createdb sabelotodo_dev
```
Now set up the tables using Alembic. 
```
python manage.py db upgrade
```
Rerun this last command after changing the models or checking out a new branch.

## Usage

Run `npm run start` to build the react app and start the Flask server (in development mode).

In a web browser, load the URL `http://127.0.0.1:3000/`. A page with a default React app appears.

### Tests
Run python tests by `running python -m pytest sabelotodo/`
Run JavaScript tests using `npm test`. (These tests will run continuously as you change the code.)

#### Adding a test fixture
When adding a fixture for use across multiple files, it must be imported to conftest.py in order to be available.

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
