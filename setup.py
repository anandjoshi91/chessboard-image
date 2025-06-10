#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version from the package
def get_version():
    version = {}
    with open(os.path.join(this_directory, 'chessboard_image', 'generator.py'), 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                exec(line, version)
                break
    return version.get('__version__', '1.1.3')

setup(
    name='chessboard-image',
    version=get_version(),
    author='Anand Joshi',
    author_email='anandhjoshi@outlook.com',
    description='Generate beautiful chess board images from FEN notation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/anandjoshi91/chessboard-image',
    project_urls={
        'Bug Reports': 'https://github.com/anandjoshi91/chessboard-image/issues',
        'Source': 'https://github.com/anandjoshi91/chessboard-image',
        'Documentation': 'https://github.com/anandjoshi91/chessboard-image#readme',
    },
    packages=find_packages(),
    package_data={
        'chessboard_image': ['theme.json', 'themes/*.json'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    keywords='chess, fen, board, image, generator, diagram, visualization',
    python_requires='>=3.7',
    install_requires=[
        'Pillow>=8.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'chessboard-image=chessboard_image.cli:main',
        ],
    },
    zip_safe=False,
)