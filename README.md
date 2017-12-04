# Vivo Sentinel

An all-powerful toolset for Vivo.

Sentinel is an autonomous agent for persisting, processing and automating Vivo V12.1 governance objects and tasks, and for expanded functions in the upcoming Vivo V13 release (Evolution).

Sentinel is implemented as a Python application that binds to a local version 12.1 vivod instance on each Vivo V12.1 Masternode.

This guide covers installing Sentinel onto an existing 12.1 Masternode in Ubuntu 14.04 / 16.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python-virtualenv

Make sure the local Vivo daemon running is at least version 12.1 (120100)

    $ vivo-cli getinfo | grep version

### 2. Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    $ git clone https://github.com/vivopay/sentinel.git && cd sentinel
    $ virtualenv ./venv
    $ ./venv/bin/pip install -r requirements.txt

### 3. Set up Cron

Set up a crontab entry to call Sentinel every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/home/YOURUSERNAME/sentinel' to the path where you cloned sentinel to:

    * * * * * cd /home/YOURUSERNAME/sentinel && ./venv/bin/python bin/sentinel.py >/dev/null 2>&1

### 4. Test the Configuration

Test the config by runnings all tests from the sentinel folder you cloned into

    $ ./venv/bin/py.test ./test

With all tests passing and crontab setup, Sentinel will stay in sync with vivod and the installation is complete

## Configuration

An alternative (non-default) path to the `vivo.conf` file can be specified in `sentinel.conf`:

    vivo_conf=/path/to/vivo.conf

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py


### License

Released under the MIT license, under the same terms as VivoCore itself. See [LICENSE](LICENSE) for more info.
