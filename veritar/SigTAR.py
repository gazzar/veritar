# -*- coding: utf-8 -*-
#
#  SigTAR: Creates a TAR archive and a file containing the md5 sums of each of
#          the archive's contents.
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

import sys
import os
import subprocess
import hashlib
from optparse import OptionParser

__version__ = "0.2.0"


def main():
    # Files and directories to be archived
    opts, args = parse_cli()

    # Set global variable VERBOSE
    global VERBOSE
    VERBOSE = opts.verbose

    progname = os.path.basename(sys.argv[0])
    log("Using %s v%s\n" % (progname, __version__))

    # Create the archive
    create_archive(opts.archfile, args)


def parse_cli():
    usage = "%prog [options] file1 file2 dir1 file3 ..."
    parser = OptionParser(usage=usage, version=__version__)
    parser.add_option(
        "-f",
        "--file",
        action="store",
        type="string",
        dest="archfile",
        metavar="path",
        help="The path to the TAR file that will be created. This is a mandatory option.",
    )
    parser.add_option(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="Print verbose messages to stdout. If not used, no informational messages will be printed, except errors.",
    )
    opts, args = parser.parse_args()
    if not args:
        parser.error("At least one file or directory must be passed as an argument.")
    elif not opts.archfile:
        parser.error(
            "A filename for the archive has not been specified. Use the -f option."
        )
    return opts, args


def create_archive(tar_file_path, args):

    # Set the path of the file containing the md5 sums
    md5_file_path = "%s.md5" % tar_file_path

    TAR_ARGS = ["tar", "-cvf", tar_file_path]

    # Add files and dirs to be archived
    TAR_ARGS.extend(args)

    # Run tar
    p = subprocess.Popen(TAR_ARGS, stdout=subprocess.PIPE)

    # Open archive and md5file
    f_md5 = open(md5_file_path, "w")

    for line in p.stdout:
        line = line.strip()

        log("==> Added: '%s'" % line)

        if os.path.isfile(line):
            log("~~> Writing md5 sum for regular file: '%s'" % line)
            f_md5.write("%s  %s\n" % (file_md5sum(line), line))

    f_md5.close()


def file_md5sum(path):
    """Returns the md5 sum of the file at 'path'.
    
    Accepts a path to a file.
    """
    # Only regular files are accepted
    if not os.path.isfile(path):
        return
    f = open(path, "rb")
    READ_BLOCK_SIZE = 10240
    m = hashlib.md5()
    data = f.read(READ_BLOCK_SIZE)
    while data:
        m.update(data)
        data = f.read(READ_BLOCK_SIZE)
    f.close()
    return m.hexdigest()


#
# Logging
#


def log(msg):
    if VERBOSE:
        sys.stdout.write("%s\n" % msg)
        sys.stdout.flush()


def error(msg):
    sys.stderr.write("ERROR: %s\n" % msg)
    sys.stderr.flush()


def warning(msg):
    sys.stderr.write("WARNING: %s\n" % msg)
    sys.stderr.flush()


if __name__ == "__main__":
    main()
