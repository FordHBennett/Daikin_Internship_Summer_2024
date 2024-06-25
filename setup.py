from setuptools import setup, find_packages

setup(
    name='mitsubishi_tag_generator',
    version='0.1',
    description='Ignition to PLC Tag Generation',
    url='https://github.com/FordHBennett/Daikin_Internship_Summer_2024',
    author='Ford Hideo Bennett',
    package_dir={'': 'src'},  # Add this line to tell setuptools where to find the packages
    packages=find_packages(where='src'),  # Adjust find_packages to look in 'src'
    install_requires=['pandas', 'numpy'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-mitsubishi-tag-generator=tag_generator.main:main',
        ],
    },
)
