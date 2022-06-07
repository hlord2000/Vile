import serial
import json
import os
import threading
from audio import AudioController
import time

class ProcessMap:
    def __init__(self):
        self.file = "./proc_map.json"
        if not os.path.exists(self.file):
            with open(self.file, 'x') as f:
                pass
            with open(self.file, 'w') as f:
                json.dump([None for x in range(6)], f)

        self.modified_time = os.path.getmtime(self.file)
        self.read_proc_map()

    def __getitem__(self, key):
        return self.proc_map[key]

    def read_proc_map(self):
        with open(self.file, "r") as f:
            self.proc_map = json.load(f)

    def check_change(self):
        next_time = os.path.getmtime(self.file)
        if self.modified_time < next_time:
            self.modified_time = next_time
            self.read_proc_map()


def main():
    proc_map = ProcessMap()

    with serial.Serial('COM9') as ser:
        while True:
            if ser.in_waiting:
                proc_map.check_change()
                command = [int(y) for y in ser.readline().split()]
                if proc_map[command[0]] == "V_SYSTEM":
                    continue
                process = AudioController(proc_map[command[0]])
                try:
                    process.set_volume(process.vol_change(command[1]))
                except TypeError:
                    pass
            time.sleep(0.05)


if __name__ == "__main__":
    main()
