"""
100 series.
"""
RESTART_MARKER_REPLY = "110 MARK {yyyy} = {mmmm}\n"
READY_IN_TIME = "120 Service ready in {nn} minutes.\n"
ALREADY_OPEN = "125 Connection already open. Transfer Starting.\n"
FILE_STATUS_OK = "150 File ok. Opening connection for data transfer.\n"


"""
200 series.
"""
COMMAND_OK = "200 OK\n"
COMMAND_NOT_IMPLEMENTED = "202 Command {cmd} not implemented on this server.\n"
SYSTEM_STATUS = "211 System status: {status}\n"
DIRECTORY_STATUS = "212 Directory status: {status}\n"
FILE_STATUS = "213 File status: {status}\n"
HELP_MESSAGE = "214 Help message: {message}\n"
SYSTEM_TYPE = "215 UNIX Type: L8\n"
SERVICE_READY_NEW_USER = "220 System ready for new user\n"
CLOSING_CONTROL_CONNECTION = "221 Closing control connection!\n"
DATA_CONNECTION_OPEN = "225 Data connection open; no transfer in progress.\n"
CLOSING_DATA_CONNECTION = "226 Closing data connection!\n"
ENTERING_PASSIVE_MODE = "227 {ip}\n"
LOGIN_SUCCESS = "230 Login success. Welcome, {user}.\n"
FILE_ACTION_OK = "250 File action ok.\n"
PRINT_WORKING_DIRECTORY = "257 \"{pathname}\".\n"


"""
300 series.
"""
USERNAME_OK = "331 User name OK.\n"
LOGIN_REQUIRED = "332 Login required.\n"
FILE_ACTION_PENDING_INFO = "350 Requested file action pending further info.\n"


"""
400 series
"""
SERVICE_UNAVAILABLE = "421 Service unavailable. Try again later.\n"
CANNOT_OPEN_DATA_CONNECTION = "425 Cannot open data connection. Try changing to PORT mode, or connect via HTTP.\n"
CONNECTION_CLOSED_TRANSFER_ABORTED = "426 Data connection was unexpectedly closed. Transfer aborted.\n"
FILE_ACTION_NOT_TAKEN = "450 File unavailable/busy. Try again later.\n"
ACTION_ABORTED = "451 Requested action aborted: local error in processing.\n"
INSUFFICIENT_STORAGE = "452 Requested action not taken. Insufficient storage space in system.\n"


"""
500 series.
"""
SYNTAX_ERROR_COMMAND = "500 Syntax error: unrecognized command.\n"
SYNTAX_ERROR_PARAMS = "501 Syntax error: bad parameter(s).\n"
COMMAND_NOT_IMPLEMENTED = "502 That command is not implemented.\n"
BAD_COMMAND_SEQUENCE = "503 Bad sequence of commands.\n"
COMMAND_NOT_IMPLEMENTED_PARAMS = "504 Command not implemented for that parameter.\n"
USER_NOT_LOGGED_IN = "530 User not logged in. Log in first.\n"
USER_STORAGE_DENIED = "532 Logged in user does not have permission to store files on remote server.\n"
NO_SUCH_FILE_OR_DIRECTORY = "550 No such file or directory.\n"
ACTION_ABORTED_STORAGE = "552 Requested file action aborted. Exceeded storage allocation.\n"
FILE_NAME_NOT_ALLOWED = "553 Requested action not taken. File name not allowed.\n"


"""
10000 series. Winsock related statuses.
"""
CONNECTION_RESET = "10054 Connection reset by peer.\n"
CANNOT_CONNECT_TIMEOUT = "10060 Cannot connect to remote server: timeout.\n"
CANNOT_CONNECT_REFUSED = "10060 Cannot connect to remote server: connection refused.\n"
CANNOT_DELETE_DIRECTORY = "10066 Directory not empty.\n"
TOO_MANY_USERS = "10068 Too many users, server is full. Try again later.\n"
