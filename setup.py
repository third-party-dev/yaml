from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="thirdparty-yaml",
    version="0.1.0",
    description="Tools for managing yaml configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vincent Agriesti",
    author_email="crazychenz@gmail.com",
    url="https://github.com/third-party-dev/yaml",
    python_requires='~=3.7',
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
    ],
)

