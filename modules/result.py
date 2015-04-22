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


class Result(object):

    def __init__(self, job, bundle):
        """
        Abstracts a LAVA result.
        :job : Job
        :bundle : Bundle
        """
        self._job = job
        self._bundle = bundle


class KernelCIResult(Result):

    def get_boot_result(self):
        """
        Returns a kernelci.org boot result.
        :rtype : dict
        """
        boot_results = self._bundle.get_boot_metadata()
        boot_results['result'] = self._job.result
        return boot_results
