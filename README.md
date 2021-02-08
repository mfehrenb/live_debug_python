# live_debug_python

## Initial Setup
1. Install docker: `https://www.docker.com/get-started`
2. Install docker compose: `https://docs.docker.com/compose/install/`
3. If on windows install make (should be there on ubuntu or mac): `http://gnuwin32.sourceforge.net/packages/make.htm`
4. Install python 3.8 for your system. For Mac we are using this `https://github.com/pyenv/pyenv`
    ```bash
    $ brew update
    $ brew install pyenv
    $ brew install zlib
    $ sudo pyenv install 3.8.6
    ```
   I hit a pyexpat issue on mac. Had to reinstall the xcode command line tools
   ```bash
    $ sudo rm -rf /Library/Developer/CommandLineTools
    $ xcode-select --install
   ```
5. Create a pipenv for the repo:
    ```bash
    $ pip3 install --upgrade pip
    $ pip3 install pipenv
    $ cd git/live_debug_python
    $ pipenv install
    ```
6. Build the docker image:
    ```bash
    $ make build
    ```

## Running tests
To run the tests within a container please do the following:
  ```bash
  $ cd git/live_debug_python
  $ make test
  ```

## Accessing the Admin Page
  ```bash
  $ cd git/live_debug_python
  $ make superuser
  $ make local
  ```
  Load the admin page using http://localhost:8000/admin/ and log in with the superuser

## Creating a user and token in the browser
1. In chrome browse to http://localhost:8000/api/v1/users/create/
2. Enter the information for the user.
3. In the browser navigate to http://localhost:8000/api/v1/users/token/
4. Enter the user information and save the token.

## Debugging the server
1. Start by enabling a django launch.json file: https://code.visualstudio.com/docs/python/tutorial-django
2. Run the db only
    ```bash
    $ make local_db_only
    ```
3. In VSCode click on the debug menu and select RUN
