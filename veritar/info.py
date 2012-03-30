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

version = '0.5.0'
status = 'alpha'
name = 'veritar'
description = """veritar"""
long_description = """veritar"""
author = 'George Notaras'
author_email = 'gnot@g-loaded.eu'
url = 'http://www.codetrax.org/projects/' + name
download_url = "http://www.codetrax.org/downloads/projects/" + name + "/" + name + "-" + version + ".tar.gz"
license = "Apache License version 2"

# Automate the development status for classifiers
devel_status = ''
if status == 'pre-alpha':
	devel_status = 'Development Status :: 2 - Pre-Alpha'
if status == 'alpha':
	devel_status = 'Development Status :: 3 - Alpha'
if status == 'beta':
	devel_status = 'Development Status :: 4 - Beta'
if status == 'stable':
	devel_status = 'Development Status :: 5 - Production/Stable'

# For a list of classifiers check: http://www.python.org/pypi/
# (http://pypi.python.org/pypi?:action=list_classifiers)

classifiers = [
	devel_status,
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

def get_version():
	return name + ' v' + version + '/' + status
