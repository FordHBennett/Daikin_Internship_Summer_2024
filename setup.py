from setuptools import setup, find_packages

setup(
    name='ignition_to_plc_tag_generation',
    version='0.1',
    description='Ignition to PLC Tag Generation',
    url='https://github.com/FordHBennett/Daikin_Internship_Summer_2024',
    author='Ford Hideo Bennett',
    packages=['ignition_to_plc_tag_generation'],
    install_requires=['pandas', 'numpy'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-tag-generation=ignition_to_plc_tag_generation.main:main',
        ],
    },
)

