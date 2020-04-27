import visa
import numpy as np
import time
import xdrlib


class SMU(object):
    class SMUChannel(object):
        def __init__(self, name, inst):
            self._name = name.lower()
            self._inst = inst

        def configure_isource(self, range=None):
            self.set_output(False)
            self._inst.write(
                (f"smu{ self._name }.source.func = " f"smu{ self._name }.OUTPUT_DCAMPS")
            )
            if range is not None:
                self._inst.write((f"smu{ self._name }.source.rangei = " f"{ range }"))
            else:
                self._inst.write(
                    (
                        f"smu{ self._name }.source.autorangei = "
                        f"smu{ self._name }.AUTORANGE_ON"
                    )
                )

        def configure_vsource(self, range=None):
            self.set_output(False)
            self._inst.write(
                (
                    f"smu{ self._name }.source.func = "
                    f"smu{ self._name }.OUTPUT_DCVOLTS"
                )
            )
            if range is not None:
                self._inst.write((f"smu{ self._name }.source.rangev = " f"{ range }"))
            else:
                self._inst.write(
                    (
                        f"smu{ self._name }.source.autorangev = "
                        f"smu{ self._name }.AUTORANGE_ON"
                    )
                )

        def set_current(self, current, vlimit=5):

            self._inst.write(f"smu{ self._name }.source.leveli = {current}")
            self._inst.write(f"smu{ self._name }.source.limitv = {vlimit}")

        def set_voltage(self, voltage, ilimit=0.1):

            self._inst.write(f"smu{ self._name }.source.levelv = {voltage}")
            self._inst.write(f"smu{ self._name }.source.limiti = {ilimit}")

        def measure_voltage(self, range=None, nplc=1):
            if range is None:
                self._inst.write(
                    (
                        f"smu{ self._name }.measure.autorangev = "
                        f"smu{ self._name }.AUTORANGE_ON"
                    )
                )
            else:
                self._inst.write((f"smu{ self._name }.measure.rangev = " f"{ range }"))
            self._inst.write(f"smu{ self._name }.measure.nplc = { nplc }")
            self._inst.write(f"val_v=smu{ self._name }.measure.v()")

            return float(self._inst.query("print(val_v)"))

        def measure_current(self, range=None, nplc=1):
            if range is None:
                self._inst.write(
                    (
                        f"smu{ self._name }.measure.autorangei = "
                        f"smu{ self._name }.AUTORANGE_ON"
                    )
                )
            else:
                self._inst.write((f"smu{ self._name }.measure.rangei = " f"{ range }"))
            self._inst.write(f"smu{ self._name }.measure.nplc = { nplc }")
            self._inst.write(f"val_i=smu{ self._name }.measure.i()")

            return float(self._inst.query("print(val_i)"))

        def set_output(self, status):
            self._inst.write(
                (
                    f"smu{ self._name }.source.output = "
                    f"smu{ self._name }.OUTPUT_{ 'ON' if status else 'OFF'}"
                )
            )

    def __init__(self, inst_str):
        self._inst_str = inst_str

    @classmethod
    def usb_device(cls, device_string):
        return cls(device_string)

    @classmethod
    def ethernet_device(cls, ip):
        return cls(f"TCPIP::{ ip }::inst0::INSTR")

    def __enter__(self):
        rm = visa.ResourceManager("@py")
        self._inst = rm.open_resource(self._inst_str)
        while True:
            try:
                time.sleep(0.1)
                self._inst.read_raw()
            except Exception:
                break

        self._inst.write("reset()")
        self._inst.write("errorqueue.clear()")

        self.A = SMU.SMUChannel("A", self._inst)
        self.B = SMU.SMUChannel("B", self._inst)
        return self

    def __exit__(self, *args):
        self.A.set_output(False)
        self.B.set_output(False)
        self._inst.close()

    def run(self, cmd):
        self._inst.write(cmd)

    def wait_for(self, seq, timeout=10):
        ts_start = time.time()
        while time.time() < (ts_start + timeout):
            try:
                recvd = self._inst.read()
                if recvd.startswith(seq):
                    return
            except xdrlib.Error:
                pass
            time.sleep(0.1)

        raise TimeoutError(msg="Timeout waiting for sequence")

    def read_values(self, converter="f", separator=", "):
        vals = self._inst.read_ascii_values(converter=converter, separator=separator)
        return np.array(vals)

    def load_script(self, filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                self._inst.write(line)
