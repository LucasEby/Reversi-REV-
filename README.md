# Reversi
An online game with server and client code to play Reversi against other players

## Setup

### Python Setup
Check if python version given in .python-version is installed on your computer. If you need to find your python installation path, type `which python` into your terminal (on Windows, git bash supports this). If you don't have the correct python version installed, download the correct version from https://www.python.org/downloads/ into the default installation location.  

### Create and activate venv
Copy your python path given by `which python`. In your terminal, type the following command. Replace "PATH_TO_REVERSI" with your **full** path to this repository and "CORRECT_PYTHON_PATH" with the output of `which python`.
```
CORRECT_PYTHON_PATH -m venv PATH_TO_REVERSI/Reversi-REV-/venv
```
Navigate in your terminal to the top-level folder of this repository. Activate your virtual environment in the terminal by running one of the following. You'll know there's success when "(venv)" shows up at the front of your terminal prompt line  
*Windows*
```
PATH_TO_REVERSI\Reversi-REV-\venv\Scripts\activate.bat
```
*Mac*
```
/venv/bin/activate
```
If neither of these work, try suggestions on this page: https://docs.python.org/3/library/venv.html

### Install requirements
In your terminal with an activated venv, install program requirements with:
```
pip install -r requirements.txt
```

## Running Program
In your terminal in the top level of the repository, the server or client code can be run using the following commands:
```
python -m client
```
```
python -m server
```