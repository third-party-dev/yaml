import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

setup(
    name="thirdparty-yaml",
    version="0.1.0",
    description="Tools for managing yaml configurations.",
    author="Vincent Agriesti",
    author_email="crazychenz@gmail.com",
    url="https://github.com/third-party-dev/yaml",
    packages=[
        "thirdparty",
        "thirdparty.yaml",
        "thirdparty.yaml.operation",
        "thirdparty.yaml.include",
        "thirdparty.yaml.include.format",
        "thirdparty.yaml.include.scheme",
        "thirdparty.yaml.tests",
    ],
    package_dir={"": "src"},
    install_requires=[
        "future",
        "ruamel.yaml",
        "pkg_resources",
    ],
    package_data={"thirdparty.yaml.tests": ["data/*.yaml", "data/*.txt"]},
)
