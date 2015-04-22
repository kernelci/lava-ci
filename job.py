from utils import is_key


class Job(object):
    def __init__(self, job, details, log):
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
        return self._log

    @property
    def bundle_id(self):
        return self._bundle_id

    @property
    def result(self):
        return self._result

    @property
    def device_type(self):
        return self._device_type

    @property
    def job_name(self):
        return self._details