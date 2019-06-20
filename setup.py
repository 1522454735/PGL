# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import re
import codecs
import numpy as np
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize

cur_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cur_dir, 'README.md'), 'rb') as f:
    lines = [x.decode('utf-8') for x in f.readlines()]
    lines = ''.join([re.sub('^<.*>\n$', '', x) for x in lines])
    long_description = lines

compile_extra_args = ["-std=c++11"]
link_extra_args = []

if sys.platform == "darwin":
    compile_extra_args = ['-std=c++11', "-mmacosx-version-min=10.9"]
    link_extra_args = ["-stdlib=libc++", "-mmacosx-version-min=10.9"]


def read(*parts):
    with codecs.open(os.path.join(cur_dir, *parts), 'r') as fp:
        return fp.read()


# Reference: https://github.com/pypa/pip/blob/master/setup.py
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M, )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


extensions = [
    Extension(
        "pgl.graph_kernel",
        ["pgl/graph_kernel.pyx"],
        language="c++",
        include_dirs=[np.get_include()],
        extra_compile_args=compile_extra_args,
        extra_link_args=link_extra_args, ),
]


def get_package_data(path):
    files = []
    print(path)
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


package_data = {'pgl': get_package_data(os.path.join(cur_dir, 'pgl/data'))}

setup(
    name="pgl",
    description='Paddle Graph Learning',
    version=find_version("pgl", "__init__.py"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/PaddlePaddle/PGL",
    package_data=package_data,
    packages=find_packages(),
    include_package_data=True,
    ext_modules=cythonize(extensions),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ], )
