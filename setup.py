from setuptools import setup, find_packages
import subprocess
import sys

def read_requirements():
    try:
        # Check if we have an internet connection
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        with open('requirements.txt') as f:
            return f.read().splitlines()
    except subprocess.CalledProcessError:
        print("No internet connection. Skipping package installations.")
        return []

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
    },
)
