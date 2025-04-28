from setuptools import setup, find_packages
import os
import re

# Hardcoded version for now
version = '1.0.3'

# Read long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="snapdroid",
    version=version,
    description="Android Screenshot and Screen Recording Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Siddharth Joshi",
    url="https://github.com/dr34mhacks/snapdroid",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "snapdroid=snapdroid.snapdroid:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.6",
    keywords="android, screenshot, screen recording, adb, testing, security",
)