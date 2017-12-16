"""
    Set up defaults and read sentinel.conf
"""
import argparse
import sys
import os
from desire_config import DesireConfig


default_sentinel_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../sentinel.conf')
)

if not os.path.isfile(default_sentinel_config):
    base = os.path.abspath(os.path.dirname(sys.argv[0]))
    default_sentinel_config = os.path.join(base, 'sentinel.conf')

sentinel_config_file = os.environ.get('SENTINEL_CONFIG', default_sentinel_config)

sentinel_cfg = DesireConfig.tokenize(sentinel_config_file)
sentinel_version = "1.1.0"
min_desired_proto_version_with_sentinel_ping = 70207


def get_argarse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=False)
    parser.add_argument('--rpc-port', type=int, required=False)
    parser.add_argument('--repair', action='store_true', default=False, required=False)
    parser.add_argument('--sentinel', action='store_true', default=False, required=False)
    return parser

def get_args():
    parser = get_argarse()

    try:
        args = parser.parse_args()
    except:
        # We are inside tests
        parser.add_argument('folder')
        args = parser.parse_args()

    return args

def get_desire_conf():
    args = get_args()

    if args.config:
        desire_conf = args.config
    else:
        home = os.environ.get('HOME')
        if home is not None:
            if sys.platform == 'darwin':
                desire_conf = os.path.join(home, "Library/Application Support/DesireCore/desire.conf")
            else:
                desire_conf = os.path.join(home, ".desirecore/desire.conf")
        else:
            home = os.getenv('APPDATA')
            if home is not None:
                desire_conf = os.path.join(home, "desirecore\\desire.conf")
            else:
                desire_conf = 'desire.conf'
        
        desire_conf = sentinel_cfg.get('desire_conf', desire_conf)

    return desire_conf


def get_network():
    return sentinel_cfg.get('network', 'mainnet')


def sqlite_test_db_name(sqlite_file_path):
    (root, ext) = os.path.splitext(sqlite_file_path)
    test_sqlite_file_path = root + '_test' + ext
    return test_sqlite_file_path


def get_db_conn():
    import peewee
    env = os.environ.get('SENTINEL_ENV', 'production')

    # default values should be used unless you need a different config for development
    db_host = sentinel_cfg.get('db_host', '127.0.0.1')
    db_port = sentinel_cfg.get('db_port', None)
    db_name = sentinel_cfg.get('db_name', 'sentinel')
    db_user = sentinel_cfg.get('db_user', 'sentinel')
    db_password = sentinel_cfg.get('db_password', 'sentinel')
    db_charset = sentinel_cfg.get('db_charset', 'utf8mb4')
    db_driver = sentinel_cfg.get('db_driver', 'sqlite')

    if (env == 'test'):
        if db_driver == 'sqlite':
            db_name = sqlite_test_db_name(db_name)
        else:
            db_name = "%s_test" % db_name

    peewee_drivers = {
        'mysql': peewee.MySQLDatabase,
        'postgres': peewee.PostgresqlDatabase,
        'sqlite': peewee.SqliteDatabase,
    }
    driver = peewee_drivers.get(db_driver)

    dbpfn = 'passwd' if db_driver == 'mysql' else 'password'
    db_conn = {
        'host': db_host,
        'user': db_user,
        dbpfn: db_password,
    }
    if db_port:
        db_conn['port'] = int(db_port)

    if driver == peewee.SqliteDatabase:
        db_conn = {}

    db = driver(db_name, **db_conn)

    return db


desire_conf = get_desire_conf()
network = get_network()
db = get_db_conn()
