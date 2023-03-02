# coding: utf-8
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer


class MyHandler(FTPHandler):
    def on_file_sent(self, file):
        # super().on_file_sent(file)
        print(f'file {file} sended')

def main():
    address = ('192.168.1.129', 2121)
    authorizer = DummyAuthorizer()
    authorizer.add_user('userftp', 'pwdftp', r'C:\projets\python\dashbd\ftp\packages', perm="elr",
                       msg_login="Login successful", msg_quit="Goodbye")
    handler=  FTPHandler
    handler.authorizer = authorizer
    with FTPServer(address, handler) as server:
        server.serve_forever()

if __name__ == "__main__":
    main()