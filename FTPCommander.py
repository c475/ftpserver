import sys
import os
import subprocess
import socket

from responses import *


class FTPCommander(object):

    def __init__(self, request, user, sys_info, sys_state, data_channel):
        self.request = request
        self.user = user
        self.sys_info = sys_info
        self.sys_state = sys_state
        self.data_channel = data_channel

        self.last_response = None


    def ABOR(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def ACCT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def ADAT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def ALLO(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def AUTH(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def CCC(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def CDUP(self, *params, **kwargs):
        """
        Basically go down one directory.
        Change this: /var/log/apache2
        Into this: /var/log
        """
        path_list = self.sys_state.working_directory.split("/")
        self.sys_state.working_directory = "/".join(path_list[:-1])
        return COMMAND_OK

    def CONF(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def CWD(self, *params, **kwargs):
        """
        Like cd command. Change the current working directory.
        """
        pathname = self.last_response[1]

        if os.path.exists(pathname):
            self.sys_state.change_directory(pathname)
            return FILE_ACTION_OK
        else:
            return NO_SUCH_FILE_OR_DIRECTORY

    def DELE(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def ENC(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def EPRT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def EPSV(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def FEAT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def HELP(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def LANG(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def LIST(self, *params, **kwargs):
        """
        Like ls command. Get a list of files in working directory.
        """

        def transfer_callback(clientsock, datasock):
            clientsock.send(FILE_STATUS_OK)

            datasock.connect(self.data_channel.address)

            datasock.send(subprocess.check_output([
                "ls",
                "-aChl",
                self.sys_state.working_directory
            ]))

            clientsock.send(CLOSING_DATA_CONNECTION)

            datasock.close()

            self.data_channel.socket = None
            self.data_channel.address = None

        return transfer_callback

    def LPRT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def LPSV(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def MDTM(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def MIC(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def MKD(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def MLSD(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def MLST(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def MODE(self, *params, **kwargs):
        """
        MODE is obsolete. Just accept with S param and do nothing.
        """
        if self.last_response[1] == "S":
            return COMMAND_OK
        else:
            return SYNTAX_ERROR_PARAMS

    def NOOP(self, *params, **kwargs):
        return COMMAND_OK

    def OPTS(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def PASS(self, *params, **kwargs):
        """
        Password handling.
        The goal of this class is to be stateless...
        Do something about stateful services like this
        """

        # for now...
        self.user.authenticated = True
        return LOGIN_SUCCESS.format(user=self.user.username)
        

    def PASV(self, *params, **kwargs):
        self.data_channel.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        
        return COMMAND_NOT_IMPLEMENTED

    def PBSZ(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def PORT(self, *params, **kwargs):
        """
        Establish connection to client-supplied address for data transfer.
        """
        # handle case where socket is already connected...

        self.data_channel.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        addr = params[0][0].split(",")
        host = ".".join(addr[:4])
        port = (int(addr[4]) * 256) + int(addr[5])

        self.data_channel.address = (host, port)

        return COMMAND_OK

    def PROT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def PWD(self, *params, **kwargs):
        """
        Print the working directory (pathname)
        """
        return PRINT_WORKING_DIRECTORY.format(
            pathname=self.sys_state.working_directory
        )

    def QUIT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def REIN(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def REST(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def RETR(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def RMD(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def RNFR(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def SITE(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def SIZE(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def SMNT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def STAT(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def STOR(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def STOU(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def STRU(self, *params, **kwargs):
        """
        STRU is obsolete. Just accept with F param and do nothing.
        """
        if self.last_response[1] == "F":
            return COMMAND_OK
        else:
            return SYNTAX_ERROR_PARAMS

    def SYST(self, *params, **kwargs):
        # semi-bogus response to keep clients happy
        return SYSTEM_TYPE

    def TYPE(self, *params, **kwargs):
        transfer_type = self.last_response[1]

        if transfer_type in ("A", "I", "L 8", "A N"):
            self.server_state.transfer_type = transfer_type
            return COMMAND_OK
        else:
            return SYNTAX_ERROR_PARAMS

    def USER(self, *params, **kwargs):
        """
        The goal of this class is to be stateless...
        Do something about stateful services like this
        """
        return USERNAME_OK

    def XCUP(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XMKD(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XPWD(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XRCP(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XRMD(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XRSQ(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XSEM(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED

    def XSEN(self, *params, **kwargs):
        return COMMAND_NOT_IMPLEMENTED
