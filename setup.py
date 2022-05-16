from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rust-macro',  # How you named your package folder (MyLib)
    packages=['rust_macro'],  # Chose the same as 'name'
    version='0.1.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='rust-macro is a library that adds the ability to create and use rust-like macros for python.',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='4gboframram',  # Type in your name
    url='https://github.com/4gboframram/py-rust-macro',  # Provide either the link to your github or to your website
    project_urls={
        'Documentation': 'https://py-rust-macro.readthedocs.io/en/latest/index.html',
        'Issue tracker': 'https://github.com/4gboframram/py-rust-macro/issues',
      },
    keywords=['python', 'macros', 'rust', 'preprocessor', 'import hook'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Pre-processors ',
        'Topic :: Utilities',
        'Typing :: Typed',
        
    ],
)
