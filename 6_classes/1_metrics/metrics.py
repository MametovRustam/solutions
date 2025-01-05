import os
import pytz
from datetime import datetime
from helpers import create_file

class ProtocolSurv:
    def save_to_file(self, buffer):
        raise NotImplementedError("This method needs to be implemented again.")

class SaverTxt(ProtocolSurv):
    def __init__(self, pathname):
        self.pathname = pathname
    def save_to_file(self, buffer):
        with open(self.pathname, "a") as file:
            for obj in buffer:
                timestamp, name, value = obj
                file.write(f"{timestamp} {name} {value}\n")
        buffer.clear()
class SaverCsv(ProtocolSurv):
    def __init__(self, pathname):
        self.pathname = pathname

    def save_to_file(self, buffer):
        with open(self.pathname, "a") as file:
            for obj in buffer:
                timestamp, name, value = obj
                file.write(f"{timestamp};{name};{value}\n")
        buffer.clear()

class Statsd:
    def __init__(self):
        self.surv = None
        self.buffer_limit = 10
        self.buffer = []

    def set_surv(self, surv):
        self.surv = surv

    def incr(self, name):
        self.create_metric(name, 1)

    def decr(self, name):
        self.create_metric(name, -1)

    def create_metric(self, name, value):
        utc_now = datetime.now(pytz.utc)
        timestamp = utc_now.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.buffer.append((timestamp, name, value))

        if len(self.buffer) >= self.buffer_limit:
            self._evacuate()

    def _evacuate(self):
        if self.surv:
            self.surv.save_to_file(self.buffer)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._evacuate()
        self.buffer.clear()

def get_txt_statsd(pathname, buffer_limit=10):
    if not pathname.endswith('.txt'):
        raise ValueError("File must be a .txt file.")
    if not os.path.isfile(pathname):
        create_file(pathname)
    surv = SaverTxt(pathname)
    statsd = Statsd()
    statsd.set_surv(surv)
    statsd.buffer_limit = buffer_limit
    return statsd
def get_csv_statsd(pathname, buffer_limit=10):
    if not pathname.endswith('.csv'):
        raise ValueError("File must be a .csv file.")
    if not os.path.isfile(pathname):
        create_file(pathname)
    if os.path.getsize(pathname) == 0:
        with open(pathname, "a") as file:
            file.write("Timestamp;Name;Value\n")
    surv = SaverCsv(pathname)
    statsd = Statsd()
    statsd.set_surv(surv)
    statsd.buffer_limit = buffer_limit
    return statsd