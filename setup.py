from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rust-macro",  # How you named your package folder (MyLib)
    packages=find_packages(),  # Chose the same as "name"
    version="0.1.0",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="rust-macro is a library that adds the ability to create rust-like macros for python.",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="4gboframram",  # Type in your name
    url="https://github.com/4gboframram/Python-Gelbooru",  # Provide either the link to your github or to your website
    # download_url='https://github.com/FujiMakoto/pygelbooru/archive/v0.3.1.tar.gz',
    keywords=["python", "macro", "rust"],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # Again, pick a license
        "Programming Language :: Python :: 3.8",
    ],
)
