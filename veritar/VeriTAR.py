# -*- coding: utf-8 -*-
#
#  veritar: In-place verification of the MD5 sums of files within a tar archive.
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

__version__ = "0.5.0"
__author__ = "George Notaras <gnot -at- g-loaded.eu>"
__credits__ = ""

import os
import sys
import tarfile
import hashlib
from optparse import OptionParser
import time
from textwrap import dedent


def err(msg, opts=None):
    """Writes 'msg' to stderr.
    """
    if not opts or not opts.quiet:
        sys.stderr.write("%s\n" % msg)
        sys.stderr.flush()

def warn(msg, opts):
    """Writes 'msg' to stderr.
    """
    if not opts.quiet:
        if not opts.nowarn:
            sys.stderr.write("%s\n" % msg)
            sys.stderr.flush()

def info(msg, opts, force=False):
    """Writes 'msg' to stdout if verbose.
    
    If force is True message is printed to stdout regardless of verbosity
    level.
    """
    if opts.verbose or force:
        sys.stdout.write("%s\n" % msg)
        sys.stdout.flush()

def get_member_md5sum(f):
    """Returns the archived file's md5 sum.
    
    Accepts the file descriptor of the tar member.
    """
    READ_BLOCK_SIZE = 65536
    def read_block():
        try:
            data_block = f.read(READ_BLOCK_SIZE)
        except IOError:
            raise IOError("Corrupted Member")
        else:
            return data_block
    m = hashlib.md5()
    data = read_block()
    while data:
        m.update(data)
        data = read_block()
    return m.hexdigest()


def get_valid_checksums(path):
    """Returns a dictionary of items: 'name:md5sum'
    
    Reads path and retrieves md5 sums and pathnames, which are stored in a
    dictionary using the format:   'name' : md5sum
    """
    csums = {}
    f_sums = open(path)
    for line in f_sums:
        if line.strip():
            try:
                csum, name = line.split("  ")
            except ValueError:
                err("ERROR: bad checksum file: %s" % path)
                sys.exit(1)
            else:
                csums[name.strip()] = csum.strip()
    f_sums.close()
    return csums


class Stats:
    """Verification statistics object
    
    Holds counters.
    Provides functions that increase each counter and also print messages.
    """
    L_JUST = 10    # Left justify position
    
    # Counters
    Processed = 0
    Good = 0
    Skipped = 0
    Corrupted = 0
    Missing = 0
    
    def __init__(self, opts):
        self.opts = opts
    
    def IncProcessed(self):
        """Increases the 'Processed' counter.
        
        Types of files that this counter counts:
            - Verified
            - Skipped
            - Failed
        
        It does not count the 'missing'
        """
        self.Processed += 1
    
    def IncGood(self, name):
        """Increases the 'Good' counter.
        
        For verified files.
        """
        info("%s %s" % ("OK".ljust(self.L_JUST), name), self.opts)
        self.Good += 1
    
    def IncSkipped(self, name, mtype):
        """Increases the Skipped counter.
        
        'Skipped' are tar members which are not regular files.
        It does not matter whether a checksum for a non-regular file
        exists. It is not an error.
        """
        warn("%s SKIPPING: %s (%s)" % (
            "WARNING".ljust(self.L_JUST), name, mtype), self.opts
        )
        self.Skipped += 1
    
    def IncCorrupted(self, name):
        err("%s %s" % ("CORRUPT".ljust(self.L_JUST), name), self.opts)
        self.Corrupted += 1
    
    def IncMissing(self, name):
        # Tar member exists, but no checksum
        # Not a TAR integrity error,
        # but md5sum file is bad
        warn("%s MISSING: %s" % (
            "WARNING".ljust(self.L_JUST), name), self.opts
        )
        self.Missing += 1

    def summary(self):
        ssw = sys.stdout.write
        title = "TAR members checksum verification"
        ssw("\n%s\n" % title)
        ssw("%s\n" % ("-" * len(title)))
        ssw("%s: %s\n" % ("Processed".ljust(self.L_JUST), self.Processed))
        ssw("%s: %s\n" % ("Verified".ljust(self.L_JUST), self.Good))
        ssw("%s: %s\n" % ("Skipped".ljust(self.L_JUST), self.Skipped))
        ssw("%s: %s\n" % ("Failed".ljust(self.L_JUST), self.Corrupted))
        ssw("%s: %s\n" % ("Missing".ljust(self.L_JUST), self.Missing))
        ssw("%s\n" % ("-" * len(title)))
        if self.Corrupted:
            ssw("FAILED")
        elif self.Missing:
            ssw("MISSING CHECKSUMS, TAR INTEGRITY OK SO FAR")
        else:
            ssw("SUCCESS")
        ssw("\n%s\n" % ("-" * len(title)))
        sys.stdout.flush()


class TarVerification:
    TAR_IGNORE_ZEROS = True
    TAR_DEBUG = 1
    TAR_ERRORLEVEL = 2
    
    def __init__(self, tarpath, checksumpath, opts):
        """Constructs the verifier object.
        
        Accepts:
            tarpath        : path to TAR archive
            checksumpath    : path to file with md5  checksums
            opts        : options
        
        self.csums : Dictionary with 'filename:md5sum'
        self.f_tar : TAR archive file object
        self.opts  : options
        self.s       : statistics object
        """
        self.csums = get_valid_checksums(checksumpath)
        self.f_tar = self.__open_archive(tarpath)
        self.type_translator = self.__get_supported_types_dict()
        self.s = Stats(opts)
        info("%s v%s\n\n" % \
        (os.path.basename(sys.argv[0]), __version__), opts, force=True)
        if opts.quiet:
            info("please wait...\n", opts, force=True)

    def __open_archive(self, tarpath):
        try:
            f_tar = tarfile.open(tarpath, "r|*")
        except tarfile.ReadError, e:
            err("ERROR: %s: %s" % (str(e)[:str(e).find(":")], tarpath))
            sys.exit(1)
        else:
            f_tar.ignore_zeros = self.TAR_IGNORE_ZEROS
            f_tar.debug = self.TAR_DEBUG
            f_tar.errorlevel = self.TAR_ERRORLEVEL
            return f_tar
    
    def __close_archive(self):
        self.f_tar.close()
    
    def __member_md5sum(self, member):
        f = self.f_tar.extractfile(member)
        try:
            checksum = get_member_md5sum(f)
        except IOError:
            f.close()
            return None
        else:
            f.close()
            return checksum

    def __get_supported_types_dict(self):
        type_translator = {}
        for t_attrib in dir(tarfile):
            if t_attrib.find("TYPE") != -1:
                if t_attrib not in ("REGULAR_TYPES", "SUPPORTED_TYPES"):
                    if not type_translator.has_key(t_attrib):
                        type_translator[getattr(tarfile, t_attrib)] = t_attrib
        return type_translator
    
    def __check_member(self, member):
        """Checks one member
        """
        self.s.IncProcessed()
        if member.isfile():
            if self.csums.has_key(member.name):
                checksum = self.__member_md5sum(member)
                if checksum == self.csums[member.name]:
                    self.s.IncGood(member.name)
                else:
                    self.s.IncCorrupted(member.name)
                del self.csums[member.name]
            else:
                self.s.IncMissing(member.name)
        else:
            if self.csums.has_key(member.name):
                del self.csums[member.name]
            self.s.IncSkipped(member.name, self.type_translator[member.type])
    
    def __process_remnants(self):
        """If the checksums-file contains more items than the TAR
        members it is assumed that the archive is corrupted.
        """
        if self.csums:
            for remnant in self.csums.keys():
                self.s.IncProcessed()
                self.s.IncCorrupted(remnant)
    def run(self):
        while True:
            try:
                member = self.f_tar.next()
            except IOError:
                # Counted in __process_remnants()
                continue
            else:
                if not member:
                    break
                else:
                    self.__check_member(member)
        self.__process_remnants()
        self.__close_archive()
        self.s.summary()


def parse_cli():
    usage = """

    %prog [options] tar_archive checksum_file

    checksum_file format:  'md5sum  path'"""
    parser = OptionParser(usage=usage, version=__version__)
    parser.add_option(
        "-v", "--verbose", action="store_true", dest="verbose",
        help="""Print all messages. Cannot be used with -q."""
    )
    parser.add_option(
        "-q", "--quiet", action="store_true", dest="quiet",
        help=dedent("""\
            Only checksum errors will be printed. Warnings are \
            suppressed.Cannot be used with - v. """
        )
    )
    parser.add_option("-n", "--no-warn", action="store_true", dest="nowarn",
        help=dedent("""\
            Warnings are suppressed. Note that using this switch \
            together with -q has absolutely no effect, since -q suppresses warnings \
            anyway. """
        )
    opts, args = parser.parse_args()
    if len(args) != 2:
        parser.error("Wrong number of arguments")
    elif opts.quiet and opts.verbose:
        parser.error("Cannot use -v and -q together.")
    elif not os.path.exists(args[0]):
        parser.error("Invalid file path: %s" % args[0])
    elif not os.path.exists(args[1]):
        parser.error("Invalid file path: %s" % args[1])
    return opts, args


def main():
    start = time.time()
    opts, args = parse_cli()
    tar_path, csum_path = args
    try:
        Verification = TarVerification(tar_path, csum_path, opts)
        Verification.run()
    except KeyboardInterrupt:
        err("Operation aborted by user", opts)
        sys.exit(1)
    else:
        finish = time.time()
        sys.stdout.write("Elapsed: %.3f sec\n" % (finish -start))
        sys.stdout.flush()



if __name__ == '__main__':
    main()

