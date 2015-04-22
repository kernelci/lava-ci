#!/usr/bin/env python
#
# This file is part of lava-ci.  lava-ci is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# Copyright Tyler Baker 2015

from utils import is_key


class Job(object):
    def __init__(self, job, details, log):
        """
        Abstracts a LAVA job.
        :job : dict
        :details : dict
        :log : basestring
        """
        self._job = job
        self._details = details
        self._log = log
        self._bundle_id = None
        self._result = None
        self._device_type = None
        self._job_name = None
        if is_key('bundle', self._job):
            self._bundle_id = self._job['bundle']
        if is_key('result', self._job):
            self._result = self._job['result']
        if is_key('requested_device_type_id', self._details):
            self._device_type = self._details['requested_device_type_id']
        if is_key('description', self._details):
            self._job_name = self._details['description']

    @property
    def log(self):
        """
        Returns a log from a LAVA job.
        :rtype : basestring
        """
        return self._log

    @property
    def bundle_id(self):
        """
        Returns a log from a LAVA job.
        :rtype : int
        """
        return self._bundle_id

    @property
    def result(self):
        """
        Returns a job result from a LAVA job.
        :rtype : basestring
        """
        return self._result

    @property
    def device_type(self):
        """
        Returns the device_type used from a LAVA job.
        :rtype : basestring
        """
        return self._device_type

    @property
    def job_name(self):
        """
        Returns a job details from a LAVA job.
        :rtype : dict
        """
        return self._details