import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from desired import DesireDaemon
from desire_config import DesireConfig


def test_desired():
    config_text = DesireConfig.slurp_config_file(config.desire_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000f79a81b6318e0f36dc486adf4bb5bb1fa34025d69b991893c42978c2027'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = DesireConfig.get_rpc_creds(config_text, network)
    desired = DesireDaemon(**creds)
    assert desired.rpc_command is not None

    assert hasattr(desired, 'rpc_connection')

    # Desire testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = desired.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert desired.rpc_command('getblockhash', 0) == genesis_hash
