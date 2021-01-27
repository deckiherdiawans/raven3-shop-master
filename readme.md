# Revota Raven3 Shop

Email builder and sender for daily shop report. Using Python Flask as web application framework.

## Installing

### Windows Machine

Create virtual environment.

    virtualenv venv

Activate virtual environment.

    venv\Scripts\activate.bat

Install autopep8 (automatically formats Python code to conform to the PEP 8), pylint (source-code, bug and quality checker).

    python -m pip install -U autopep8
    python -m pip install -U pylint

Install requirements

    pip install -r requirements.txt

### OSX

Oneliner

    python3 -m venv venv; source venv/bin/activate; pip install --upgrade pip; python -m pip install -U autopep8; python -m pip install -U pylint; pip install -r requirements.txt;

Create virtual environment.

    python3 -m venv venv

Activate virtual environment.

    source venv/bin/activate

Install autopep8 (automatically formats Python code to conform to the PEP 8), pylint (source-code, bug and quality checker).

    python -m pip install -U autopep8
    python -m pip install -U pylint

Install requirements

    pip install -r requirements.txt

## Running Server

Activate virtual environment first.

### Windows Machine

    python main.py

Expected result

    (env) C:\raven3-shop>python main.py
     * Serving Flask app "main.py"
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

### OSX

    env FLASK_APP=main.py flask run

Expected result

    (venv) $ env FLASK_APP=main.py flask run
     * Serving Flask app "main.py"
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

## Make Executable

    pyinstaller --onefile --icon=static/icon.ico --name raven3-shop main.py

Copy config.rvt and templates/ directory, on the same directory as exe built.

## Links

* Creation of virtual environments: <https://docs.python.org/3/library/venv.html>
* Website: <https://palletsprojects.com/p/flask/>
* Documentation: <https://flask.palletsprojects.com/>
* Releases: <https://pypi.org/project/Flask/>
* Code: <https://github.com/pallets/flask>
* Issue tracker: <https://github.com/pallets/flask/issues>
* Test status: <https://dev.azure.com/pallets/flask/_build>
* Official chat: <https://discord.gg/t6rrQZH>
* WSGI: <https://wsgi.readthedocs.io>
* Werkzeug: <https://www.palletsprojects.com/p/werkzeug/>
* Jinja: <https://www.palletsprojects.com/p/jinja/>
* pip: <https://pip.pypa.io/en/stable/quickstart/>
