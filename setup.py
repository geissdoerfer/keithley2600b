import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

requirements = ["numpy", "pyvisa-py"]

setup(
    name="keithley2600b",
    version="0.0.1",
    description="Python API for Keithley Series 2600B SourceMeter",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["keithley2600b"],
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
    ],
    install_requires=requirements,
    author="Kai Geissdoerfer",
    author_email="kai.geissdoerfer@tu-dresden.de",
)