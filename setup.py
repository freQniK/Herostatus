# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md', encoding="utf-8") as f:
    readme = f.read()

setup(
    name='Herostatus',
    version='0.3.0',
    description='Herominers console status and stats display for cryptonight miners',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='freQniK',
    author_email='freqnik@mathnodes.com',
    url='https://github.com/freqnik/herostatus',
    license='GPLv3',
    keywords='crypto cryptonight zephyr bitcoin monero haven dero ergo blockchain mining randomx',
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['requests',  'pygame'],
    package_data={'herostatus': ['logo.uni'], 'herostatus/sounds' : ['burglaralarm.wav', 'caralarm.wav', 'hiphopalarm.wav', 'sirenalarm.wav', 'strongbadalarm.wav']},
    entry_points = {
        'console_scripts': ['herostatus = herostatus.herostatus:main'],
    }
)

