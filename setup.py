from setuptools import setup, find_packages

setup(
    name='mitsubishi_tag_generator',
    version='0.1',
    description='Ignition to PLC Tag Generation',
    url='https://github.com/FordHBennett/Daikin_Internship_Summer_2024',
    author='Ford Hideo Bennett',
    packages=['mitsubishi_tag_generator'],
    install_requires=['pandas', 'numpy'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-mitsubishi-tag-generator=mitsubishi_tag_generator.main:main',
        ],
    },
)

