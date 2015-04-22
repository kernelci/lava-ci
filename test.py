from modules.bundle import *
from modules.job import *
from modules.connection import *
from modules.result import *
from modules.utils import *


def parse_json(json):
    jobs = load_json(json)
    connection = Connection(jobs['username'], jobs['token'], jobs['server'])
    connection.connect()
    duration = jobs['duration']
    # Remove unused data
    jobs.pop('duration')
    jobs.pop('username')
    jobs.pop('token')
    jobs.pop('server')
    return connection, jobs, duration

connection, jobs, duration = parse_json(os.path.join(os.path.curdir, 'bundle.json'))
for job_id in jobs:
    job_details = connection.get_job_details(job_id)
    job_log = connection.get_job_log(job_id)
    job = Job(jobs[job_id], job_details, job_log)
    bundle_id = job.bundle_id
    if bundle_id:
        json_bundle = connection.get_bundle(bundle_id)
        bundle = KernelCIBundle(json_bundle)
        print KernelCIResult(job, bundle).get_boot_result()