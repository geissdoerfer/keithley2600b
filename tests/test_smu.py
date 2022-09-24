import pytest
import pyvisa

from keithley2600b import SMU


class FakeInstrument(object):
    def write(self, cmd):
        pass

    def read(self):
        raise NotImplementedError()

    def read_raw(self, n_bytes):
        raise NotImplementedError()

    def close(self):
        pass


class FakeResourceManager(object):
    def __init__(self, *arg):
        pass

    def open_resource(self, *arg):
        return FakeInstrument()


def test_instantiation(monkeypatch):
    monkeypatch.setattr(pyvisa, "ResourceManager", FakeResourceManager)
    with SMU.ethernet_device("192.168.1.108") as smu:
        pass
