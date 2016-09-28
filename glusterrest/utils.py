# -*- coding: utf-8 -*-
#
#  Copyright (c) 2016 Red Hat, Inc. <http://www.redhat.com>
#  This file is part of GlusterFS.
#
#  This file is licensed to you under your choice of the GNU Lesser
#  General Public License, version 3 or any later version (LGPLv3 or
#  later), or the GNU General Public License, version 2 (GPLv2), in all
#  cases as published by the Free Software Foundation.
#

import fcntl
import os


class LockedOpen(object):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.open_args = args
        self.open_kwargs = kwargs
        self.fileobj = None

    def __enter__(self):
        """
        If two processes compete to update a file, The first process
        gets the lock and the second process is blocked in the fcntl.flock()
        call. When first process replaces the file and releases the lock,
        the already open file descriptor in the second process now points
        to a  "ghost" file(not reachable by any path name) with old contents.
        To avoid that conflict, check the fd already opened is same or
        not. Open new one if not same
        """
        f = open(self.filename, *self.open_args, **self.open_kwargs)
        while True:
            fcntl.flock(f, fcntl.LOCK_EX)
            fnew = open(self.filename, *self.open_args, **self.open_kwargs)
            if os.path.sameopenfile(f.fileno(), fnew.fileno()):
                fnew.close()
                break
            else:
                f.close()
                f = fnew
        self.fileobj = f
        return f

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.fileobj.close()
