import os
from setuptools import setup
from setuptools import find_packages

def _get_version():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root_dir, 'watson_nlc_wrapper', 'version.py')) as f:
        exec(f.read())
        return __version__

setup(
    name = "Watson NLC Wrapper",
    version = _get_version(),
    description = "",
    long_description = "",
    author = "Hirotaka Suzuki",
    author_email = "hirotaka.suzuki@kofearistokrat.com",
    lisense = "MIT",
    packages = find_packages(),
    url = "https://github.com/hirotaka-s/nlc_driver",
    install_requires = open('requirements.txt').read().splitlines(),
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
