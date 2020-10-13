# Atlas Automation Testing
An automation testing repository for Atlas' applications using Python, Pytest, and Selenium.

1. [Installation](#installation)
2. [Running Tests](#running-tests)
3. [Troubleshooting](#troubleshooting)

## Installation
To begin running tests, simply ensure that your Transloc virtual environment has up to date Python
dependencies by installing via `/python/requirements.txt`, then install Chromedriver:
```
webdriverdownloader chrome
```

Once chromedriver is installed, add the path to your bash_profile by running `open ~/.bash_profile`

Add the following:

```
export PATH=$PATH:/Users/{your_terminal_name}/bin
```

Then save and exit. Once done, source the profile: `source ~/.bash_profile`

## Running Tests
In order to run automation tests, a `.env` file must be created within the `/python/tests/automation/`
root. Contact a QA engineer in order to obtain the values for each field. Your `.env` file should
resemble the following:
```
AGENCY=imperialdemo
ENV=dev
HEADLESS=True
PORT=8080
TEAM=mamlambo

ADMIN_USERNAME={username}
ADMIN_PASSWORD={password}
AGENT_USERNAME={username}
AGENT_PASSWORD={password}
AUTH_TOKEN={"value": ""}
DEFAULT_API_PASSWORD={api password}
DEFAULT_PASSWORD={password}
DEFAULT_USERNAME={username}
DISPATCHER_USERNAME={username}
DISPATCHER_PASSWORD={password}
DRIVER_USERNAME={username}
DRIVER_PASSWORD={password}
RIDER_USERNAME={username}
RIDER_PASSWORD={password}
SUPERUSER_AUTH_TOKEN={"value": ""}
SUPERUSER_USERNAME={username}
SUPERUSER_PASSWORD={password}
```

Pytest will automatically run against the `.env` file using the pytest-dotenv plugin. By default,
Pytest will run tests headlessly unless "headed" is inserted into the BROWSER variable or passed as
a command line argument.

From your terminal inside of the `/python/tests/automation/` root, input the following:

```
pytest
```

This will run tests within an instance of Google Chrome. This test run will be the same as running
the following in your terminal:

```
AGENCY=imperialdemo ENV=dev HEADLESS=true PORT=8080 TEAM=mamlambo pytest
```

### Supported .env Values
The following values are currently supported:
```
HEADLESS - True, False
ENV - "dev", "localhost", "stage"
TEAM - "bloop", "kraken", mamlambo", "thunderbird"
```

All other values are not validated. In order to avoid errors, ensure that you input valid entries
for both AGENCY and PORT.

### Running Tests using Makefile
To run tests using the Transloc Makefile, simply input the following from the `transloc/` root:
```
make testui
```

The Makefile will run all tests within the automation battery using four parallel runners. An html
report will generate upon completion at `/python/tests/automation/output/`.

### Running Tests using Localhost
To run against local, set the ENV to "localhost" and provide a port to listen in to. Once modified,
run the tests as you normally would.
```
ENV=localhost PORT=8080 pytest
```

### Running Tests in Headed Format
To run tests in headed format, set the HEADLESS variable to False.

```
HEADLESS=false pytest
```

### Running Tests in Parallel
Parallelization is provided with the pytest-xdist plugin. To run tests in parallel, add the
following to the base command found above:
```
-n {number_of_processors}
```

Parallelization may also be provided through Python subprocesses. To utilize subprocesses, add the
following to the base `pytest` command:
```
--dist={load_or_each} --tx '{number_of_subprocs}*popen//python={python_path}'
```

The most efficient set up is to run automation using four cores or subprocesses (`-n 4`) as
parallelization suffers from diminishing returns. While additional cores may be used, the time
reduction is seconds compared to minutes when four cores are used. In addition, auto may be used
for pytest-xdist. In this configuration, pytest-xdist will automatically determine the number of
cores for the machine, then allocate tests to each worker.

*Caution when using auto with -n as maxing the number of cores available may cause instability.*

## Troubleshooting

### Installation
Should your installation steps fail from Sec. 1, proceed to follow these guidelines:

#### Verify your python install is using version 3.6.9
Run the following command:
```
python --version
```

If properly installed and sourced, the readout should print 'Python 3.6.9' in your terminal. If not,
try sourcing your Pyenv install with the following:

```
pyenv global 3.6.9
python --version
```

#### Verify your python install is using Pyenv as the source
Run the following command:
```
which python
```

If properly sourced, the readout should print `/Users/{user}/.pyenv/shims/python` in your terminal.
If not, try sourcing your Pyenv install with the following:

```
pyenv global 3.6.9
which python
```

#### Verify your virtualenv is using Pyenv as the source
Run the following command:
```
source ~/{virtualenv_directory}/transloc/bin/activate
which python
```

If properly sourced and installed, the readout should print the following in your terminal:

`/Users/{user}/{virtualenv_directory}/transloc/bin/python`

If not, you will have to remove the existing virtual environment and proceed with a fresh virtual
environment creation.
