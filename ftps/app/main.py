import os
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import TLS_FTPHandler
import logging
import datetime

if os.name == 'nt':
    from pyftpdlib.authorizers import DummyAuthorizer
else:
    from pyftpdlib.authorizers import UnixAuthorizer
    from pyftpdlib.filesystems import UnixFilesystem

now = datetime.datetime.now()
file = now.strftime("%Y%m%d")
filename= os.path.join(os.getcwd(), f'log/ftps_{file}.log')
logging.basicConfig(filename=filename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def main():
    if os.name == 'nt':
        authorizer = DummyAuthorizer()
    else:
        authorizer = UnixAuthorizer(rejected_users=["root"], require_valid_shell=True)
    authorizer.add_user('userftp', 'pwdftp', '.', perm='elradfmwMT')
    authorizer.add_anonymous('.')
    handler = TLS_FTPHandler
    handler.certfile = 'keycert.pem'
    handler.authorizer = authorizer
    if os.name != 'nt':
        handler.abstracted_fs = UnixFilesystem
    # requires SSL for both control and data channel
    #handler.tls_control_required = True
    #handler.tls_data_required = True
    server = FTPServer(('192.168.1.129', 21), handler)
    server.serve_forever(handle_exit=True)

if __name__ == '__main__':
    main()