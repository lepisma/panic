"""
Usage: panic [--thresh=<thresh>]

Options:
  -h --help              Show help
  --thresh=<thresh>      Percent memory usage to watch over [default: 80]
"""

import time
import psutil
import sys
from collections import deque
from docopt import docopt
from sh import notify_send

POLL_TIME = 2

class MemoryState:

    def __init__(self):
        self.history = deque(maxlen=5)
        self.last = 0

    def track(self, thresh):
        while True:
            time.sleep(POLL_TIME)
            usage = self.usage
            self.history.append(usage - self.last)
            self.last = usage

            if len([h for h in self.history if h > 1]) > 4:
                self.notify()
            elif usage > thresh:
                self.notify()

    def notify(self):
        offender = self.offender
        notify_send(
            "Memory warning",
            f"{offender.name()} [{offender.pid}] is taking too\
            much memory ({offender.memory_full_info().uss / 1024 / 1024} MBs)"
        )

    @property
    def usage(self):
        return psutil.virtual_memory().percent

    @property
    def offender(self):
        self.history.clear()
        pids = psutil.pids()

        def _get_memory(pid):
            try:
                return psutil.Process(pid).memory_percent("uss")
            except:
                return 0

        return psutil.Process(max(pids, key=lambda p: _get_memory(p)))

def main():
    args = docopt(__doc__, argv=sys.argv[1:])
    thresh = int(args["--thresh"])

    mem = MemoryState()
    mem.track(thresh)
