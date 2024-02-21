#!/usr/bin/env python3
from setuptools import setup, find_packages
import glob

setup(
  name="terminal-games",
  version="1.0.1",
  package_dir={"":"lib"},
  packages=find_packages(where="lib"),
  scripts=glob.glob("bin/*.py"),
)
