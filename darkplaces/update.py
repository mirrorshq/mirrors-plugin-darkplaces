#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import time
import subprocess
import mirrors.plugin


class Main:

    def __init__(self, sock):
        self.sock = sock
        self.dataDir = mirrors.plugin.params["storage-file"]["data-directory"]

    def run(self):
        file1 = "https://icculus.org/twilight/darkplaces/files/rygel-dp-texturepack-high.pk3"
        file2 = "https://icculus.org/twilight/darkplaces/files/rygel-dp-texturepack-ultra.pk3"

        print("Downloading file1")
        localFile1 = os.path.join(self.dataDir, "rygel-dp-texturepack-high.pk3")
        Util.wgetDownload(file1, localFile1)

        print("Downloading file2")
        localFile2 = os.path.join(self.dataDir, "rygel-dp-texturepack-ultra.pk3")
        Util.wgetDownload(file2, localFile2)


class Util:

    @staticmethod
    def cmdExec(cmd, *kargs):
        # call command to execute frontend job
        #
        # scenario 1, process group receives SIGTERM, SIGINT and SIGHUP:
        #   * callee must auto-terminate, and cause no side-effect
        #   * caller must be terminate AFTER child-process, and do neccessary finalization
        #   * termination information should be printed by callee, not caller
        # scenario 2, caller receives SIGTERM, SIGINT, SIGHUP:
        #   * caller should terminate callee, wait callee to stop, do neccessary finalization, print termination information, and be terminated by signal
        #   * callee does not need to treat this scenario specially
        # scenario 3, callee receives SIGTERM, SIGINT, SIGHUP:
        #   * caller detects child-process failure and do appopriate treatment
        #   * callee should print termination information

        # FIXME, the above condition is not met, FmUtil.shellExec has the same problem

        ret = subprocess.run([cmd] + list(kargs), universal_newlines=True)
        if ret.returncode > 128:
            time.sleep(1.0)
        ret.check_returncode()

    @staticmethod
    def wgetDownload(url, localFile):
        param = ["-t", "0", "-w", "60", "--random-wait", "-T", "60", "--passive-ftp", "--no-check-certificate"]
        if os.path.exists(localFile):
            param.append("-c")
        Util.cmdExec("/usr/bin/wget", *param, "-O", localFile, url)


###############################################################################

if __name__ == "__main__":
    with mirrors.plugin.ApiClient() as sock:
        try:
            Main(sock).run()
            sock.progress_changed(100)
        except Exception:
            sock.error_occured(sys.exc_info())
            raise
