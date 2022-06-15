from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.0.1' 
DESCRIPTION = 'Wrapper for Panduza MQTT Calls'
LONG_DESCRIPTION = 'This library provides simple wrapper to help implementing tests through panduza interfaces'

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

# Setting up
setup(
        name="panduza", 
        version=VERSION,
        author="Panduza Team",
        author_email="panduza.team@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        cmdclass={'install': CustomInstallCommand},

        install_requires=['paho-mqtt'],

        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            'Operating System :: POSIX',
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

