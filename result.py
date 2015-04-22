class Result(object):

    def __init__(self, job, bundle):
        self._job = job
        self._bundle = bundle


class KernelCIResult(Result):

    def get_boot_result(self):
        boot_results = self._bundle.get_boot_metadata()
        boot_results['result'] = self._job.result
        return boot_results
