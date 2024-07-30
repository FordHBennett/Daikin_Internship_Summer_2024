from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='tag_generator',
    version='0.1',
    description='Ignition to PLC Tag Generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FordHBennett/Daikin_Internship_Summer_2024',
    author='Ford Hideo Bennett',
    author_email='ford660bennett@tamu.edu',  # Add a contact email
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'deepdiff>=5.0.2',

    ],
    python_requires='>=3.6',  # Specify the Python versions you support
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Update to your actual license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='PLC, Ignition, tag generation, automation',
    zip_safe=False
)

