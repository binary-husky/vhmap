import os, sys
import argparse
from vhmap.mcom import *
from vhmap.mcom_replay import RecallProcessThreejs
from vhmap.utils.network import find_free_port


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HMP')
    parser.add_argument('-f', '--file', help='Directory of chosen file', default='TEMP/v2d_logger/backup.dp.gz')
    parser.add_argument('-p', '--port', help='The port for web server')
    args, unknown = parser.parse_known_args()
    if hasattr(args, 'file'):
        path = args.file
    else:
        assert False, (r"parser.add_argument('-f', '--file', help='The node name is?')")

    if hasattr(args, 'port') and args.port is not None:
        port = int(args.port)
    else:
        port = find_free_port()
        print('no --port arg, auto find:', port)

    load_via_json = (hasattr(args, 'cfg') and args.cfg is not None)
    
    rp = RecallProcessThreejs(path, port)
    rp.start()
    rp.join()
