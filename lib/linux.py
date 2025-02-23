import os
import subprocess
import platform
from utils.custom_logger import log


class Host:
    def __init__(self):
        self.is_windows = platform.system().lower() == "windows"

    def execute(self, command):
        """Executes a command based on the OS."""
        shell_type = "powershell" if self.is_windows else "bash"
        try:
            # Using subprocess to execute the command
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                executable=shell_type,
            )
            log.debug({"command:": command, "output": result.stdout, "error": result.stderr})
            return {"output": result.stdout, "error": None}
        except subprocess.CalledProcessError as e:
            return {"output": None, "error": e.stderr}


class Linux(Host):
    def __init__(self, hostname, username, password=None, key_filename=None, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = None

    def _connect(self):
        pass


if __name__ == "__main__":
    host = Host()
    host.execute("pwd")
