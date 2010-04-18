#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  VeriTAR: In-place verification of the MD5 sums of files within a tar archive.
#
#  Project: https://www.codetrax.org/projects/veritar
#
#  Copyright 2007 George Notaras <gnot [at] g-loaded.eu>, CodeTRAX.org
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
#    python setup.py install
#  Or:
#    python setup.py install --prefix=/usr
#

from distutils.core import setup
from VeriTAR import __version__

p_name = "veritar"
p_version = __version__
p_desc_short = "In-place verification of the MD5 sums of files within a tar archive"
p_desc_long = """VeriTAR description
VeriTAR [Veri(fy)TAR] is a command-line utility that verifies the md5 sums of
files within a TAR archive. Due to the tar ('ustar') format limitations the md5
sums are retrieved from a separate file and are checked against the md5 sums of
the files within the tar archive. The process takes place without actually
exctracting the files.

It works with corrupted tar archives. The program carries on to the next
file within the archive skipping the damaged parts. At the moment, this relies 
on Python's tarfile module internal functions.

Compressed TAR archives (Gzip or BZ2) are supported.

VeriTAR is written in Python.
"""
p_author = "George Notaras, G-Loaded.eu, CodeTRAX.org"
p_author_email = "<gnot [at] g-loaded.eu>"
p_url = "https://www.codetrax.org/projects/" + p_name
p_download_url = "http://www.codetrax.org/downloads/projects/" + p_name + "/" + p_name + "-" + p_version + ".tar.gz"
p_license = "Apache License version 2"
p_classifiers = [
	"Development Status :: 3 - Alpha",
	"Environment :: Console",
	"Intended Audience :: Information Technology",
	"Intended Audience :: Developers",
	"Intended Audience :: System Administrators",
	"License :: OSI Approved :: Apache Software License",
	"Natural Language :: English",
	"Operating System :: OS Independent",
	"Programming Language :: Python",
	"Topic :: System :: Archiving",
	"Topic :: Utilities",
	]

if __name__=='__main__':
	setup(
		name = p_name,
		version = p_version,
		description = p_desc_short,
		long_description = p_desc_long,
		author = p_author,
		author_email = p_author_email,
		url = p_url,
		download_url = p_download_url,
		license = p_license,
		classifiers = p_classifiers,
		py_modules = ["VeriTAR"],
		scripts = ['veritar']
		)

