#!/usr/bin/env python3
from setuptools import setup, find_packages
import glob

setup(
  name="card-games",
  version="1.0.0",
  package_dir={"":"lib"},
  packages=find_packages(where="lib"),
  scripts=glob.glob("bin/*.py"),
)
