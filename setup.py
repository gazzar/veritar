# -*- coding: utf-8 -*-
#
#  This file is part of veritar.
#
#  veritar -
#
#  Project: https://www.codetrax.org/projects/veritar
#
#  Copyright 2009 George Notaras <gnot [at] g-loaded.eu>, CodeTRAX.org
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  NOTES
#
#  Create source distribution tarball:
#    python setup.py sdist --formats=gztar
#
#  Create binary distribution rpm:
#    python setup.py bdist --formats=rpm
#
#  Create binary distribution rpm with being able to change an option:
#    python setup.py bdist_rpm --release 7
#
#  Test installation:
#    python setup.py install --prefix=/usr --root=/tmp
#
#  Install:
#    pip install
#  Or:
#    pip install --prefix=/usr
#


from distutils.core import setup

# from setuptools import setup
from veritar import info

if __name__ == "__main__":
    setup(
        name=info.name,
        version=info.version,
        description=info.description,
        long_description=info.long_description,
        author=info.author,
        author_email=info.author_email,
        url=info.url,
        download_url=info.download_url,
        license=info.license,
        classifiers=info.classifiers,
        packages=["VeriTAR"],
        scripts=["scripts/veritar", "scripts/sigtar"],
    )
