[![PyPiVersion](https://img.shields.io/pypi/v/keithley2600b.svg)](https://pypi.org/project/keithley2600b)
[![Pytest](https://github.com/geissdoerfer/keithley2600b/actions/workflows/python-tests.yml/badge.svg)](https://github.com/geissdoerfer/keithley2600b/actions/workflows/python-tests.yml)
[![CodeStyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Introduction

*The code in this repository is superseded by [this package](https://github.com/OE-FET/keithley2600).*

Keithley 2600B are a series of programmable sourcemeters.
They can be accessed remotely via a VISA interface.
The programming relies on the builtin TSP script engine which uses a LUA-style syntax.

This package provides a python API for convenient remote programming of the SMU via Ethernet/USB.