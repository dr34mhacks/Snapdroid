from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join('snapdroid', '__init__.py'), 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    version = version_match.group(1) if version_match else '0.0.0'

# Read long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="snapdroid",
    version=version,
    description="Android Screenshot and Screen Recording Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sid Joshi",
    author_email="your.email@example.com",
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