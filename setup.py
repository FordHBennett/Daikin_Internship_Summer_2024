from calendar import c
import os
import pathlib
import sys
import subprocess
from setuptools import setup, find_packages

def read_requirements():
    requirements = []
    current_dir = pathlib.Path(__file__).resolve().parent
    # if current_dir has a cache directory, install from cache
    if (current_dir / 'cache').is_dir():
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-index', '--find-links', 'cache', '-r', 'requirements.txt'])
    else:
        # Attempt to upgrade pip and install requirements if we have an internet connection
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
        # Install the requirements from the file
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + requirements)

setup(
    name='ignition_to_plc_tag_generation',
    version='0.1',
    description='Ignition to PLC Tag Generation',
    url='https://github.com/FordHBennett/Daikin_Internship_Summer_2024',
    author='Ford Hideo Bennett',
    packages=find_packages(),
    zip_safe=False,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'run-tag-generation=ignition_to_plc_tag_generation.main:main',
        ],
    }
)
