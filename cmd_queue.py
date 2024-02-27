import subprocess
import queue
import time
import os
import sys
import getopt
from Logger import log


def usage():
    log.info("""
    cmd_queue.py is the script that queues up commands to be executed in cmd.exe
    To use the script, save your commands in a text file separated by a new line

    Example: python cmd_queue.py -p [full_path of the txt file]
        such as python cmd_queue.py -p C:/test/cmds_to_run.txt
    """)


def Parse_Arguments():
    argsDefined = "p:h"
    try:
        opts, args = getopt.getopt(sys.argv[1:], argsDefined)
    except getopt.GetoptError as e:
        log.error(e)
        usage()
        sys.exit(1)

    path = ""

    for opt, arg in opts:
        if opt in('-p'):
            path = arg
        elif opt in('-h'):
            usage()
            sys.exit()

    if path == "" or not os.path.exists(path):
        log.error("ERROR: (-p) path or file not given, or doesn't exist")
        usage()
        sys.exit(1)

    if not os.path.isfile(path) or not path.endswith(".txt"):
        log.error("ERROR: (-p) path needs to be a text file if regex is not provided.")
        usage()
        sys.exit(1)

    return path


class CommandQueue:
    def __init__(self, path):
        self.cmd_queue = queue.Queue()
        self.current_cmd = None
        self.path = path


    def check_for_new_cmd(self):
        if os.path.getmtime(self.path) == self.last_modified:
            return

        self.last_modified = os.path.getmtime(self.path)
        with open(self.path) as f:
            data = f.readlines()

        try:
            last_command = data[self.total_cmds]
            if not last_command == data[self.total_cmds]:
                log.debug(f"data: {data[self.total_cmds]} not equal to last command: ")
                return
            for cmd in data[self.total_cmds:]:
                log.debug(f"Adding command: {cmd}")
                self.cmd_queue.put(cmd)
                self.total_cmds += 1

        except Exception as e:
            log.error(e)


    def main(self):
        self.last_modified = os.path.getmtime(self.path)
        with open(self.path) as r:
            data = r.readlines()
        for line in data:
            self.cmd_queue.put(line)

        self.total_cmds = len(self.cmd_queue.queue)
        log.debug(f"{len(self.cmd_queue.queue)} commands to run ...")
        log.debug(self.cmd_queue.queue)

        while not self.cmd_queue.empty():
            self.current_cmd = self.cmd_queue.get()
            if not self.current_cmd.endswith("\n"):
                self.current_cmd += "\n"

            if self.current_cmd.startswith("P>"):
                log.debug(self.current_cmd[2:])
                eval(self.current_cmd[2:].strip())
            else:
                self.cmd_line = subprocess.Popen(self.current_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                for line in self.cmd_line.stdout:
                    print(line.decode(), end="")
                self.cmd_line.stdout.close()
                return_code = self.cmd_line.wait()
                if return_code:
                    raise subprocess.CalledProcessError(return_code, self.current_cmd)
            self.check_for_new_cmd()


path = Parse_Arguments()
cmdQueue = CommandQueue(path=path)

if __name__ == '__main__':
    cmdQueue.main()
