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
from daemonize import Daemonize
from docopt import docopt
from sh import notify_send


class Tracker:

    def __init__(self, thresh, window_size=5, poll_time=2):
        self.history = deque(maxlen=window_size)
        self.last = 0
        self.hold = 0
        self.thresh = thresh
        self.window_size = window_size
        self.poll_time = poll_time

    def track(self):
        while True:
            time.sleep(self.poll_time)
            usage = self.usage
            self.history.append(usage - self.last)
            self.last = usage

            if self.hold == 0:
                if sum([h > 1 for h in self.history]) == self.window_size:
                    self.notify()
                elif usage > self.thresh:
                    self.notify()
            else:
                self.hold -= 1

    def notify(self):
        self.hold = self.window_size
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
    tracker = Tracker(thresh)

    pid = "/tmp/panic.pid"
    Daemonize(app="panic", pid=pid, action=tracker.track).start()
