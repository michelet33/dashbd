# coding: utf-8
import os
import json
import datetime
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
if os.name == 'nt':
    from pyftpdlib.authorizers import DummyAuthorizer
else:
    from pyftpdlib.authorizers import UnixAuthorizer
    from pyftpdlib.filesystems import UnixFilesystem
import requests
import logging

now = datetime.datetime.now()
file = now.strftime("%Y%m%d")
filename= os.path.join(os.getcwd(), f'log/ftp_{file}.log')
logging.basicConfig(filename=filename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

LOGIN_ENDPOINT = "http://192.168.1.129:5000"

def save_logs(msg):
    try:
        data = {"charger_id": '',
                "message_type_id": 0,
                "action": "ftpserver",
                "content": f"{msg}",
                "unique_id":''}
        djson = json.dumps(data)
        # the following line is responsible for suppressing the warning.
        requests.packages.urllib3.disable_warnings()
        response = requests.post(
           url=f"{LOGIN_ENDPOINT}/log/add/",
           data= djson,
           timeout= 30,
           verify = False
        )

        response.raise_for_status()
    except requests.HTTPError as error:
        print(error)
class MyHandler(FTPHandler):

    def on_login_failed(self, username, password):
        msg = f'Connection failed: {username} / {password}'
        save_logs(msg)

    def on_login(self, username):
        msg = f'[{username}] logged in'
        save_logs(msg)

    def on_logout(self, username):
        msg = f'[{username}] log out'
        save_logs(msg)

    def on_disconnect(self):
        msg = 'FTP session closed'
        save_logs(msg)

    def on_file_sent(self, file):
        # super().on_file_sent(file)
        msg = f"Package '{file}' sended"
        save_logs(msg)

    def on_incomplete_file_sent(self, file):
        msg = f'Package {file} incompletely sended'
        logging.error(msg)
        save_logs(msg)

def main():
    address = ('192.168.1.129', 2121)
    if os.name == 'nt':
        authorizer = DummyAuthorizer()
    else:
        authorizer = UnixAuthorizer(rejected_users=["root"], require_valid_shell=True)

    authorizer.add_user('userftp', 'pwdftp', '.', perm="elradfmwMT",
                       msg_login="Login successful", msg_quit="Goodbye")
    handler=  MyHandler
    handler.authorizer = authorizer
    if os.name != 'nt':
        handler.abstracted_fs = UnixFilesystem

    # set limit upload and download
    # dtp_handler = ThrottledDTPHandler
    # dtp_handler.read_limit = 30720  # 30 Kb/sec (30 * 1024)
    # dtp_handler.write_limit = 30720
    # handler.dtp_handler = dtp_handler

    with FTPServer(address, handler) as server:
        server.serve_forever(handle_exit=True)

if __name__ == "__main__":
    main()