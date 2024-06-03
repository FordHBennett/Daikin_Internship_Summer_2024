from setuptools import setup, find_packages

setup(
    name='ignition_to_plc_tag_generation',
    version='0.1',
    description='Ignition to PLC Tag Generation',
    url='https://github.com/FordHBennett/Daikin_Internship_Summer_2024',
    author='Ford Hideo Bennett',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'pandas',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'run-tag-generation=ignition_to_plc_tag_generation.main:main',
        ],
    },
)