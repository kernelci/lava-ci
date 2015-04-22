from bundle import *
from job import *
from result import *
from utils import *

def parse_json(json):
    jobs = load_json(json)
    url = validate_input(jobs['username'], jobs['token'], jobs['server'])
    connection = connect(url)
    duration = jobs['duration']
    # Remove unused data
    jobs.pop('duration')
    jobs.pop('username')
    jobs.pop('token')
    jobs.pop('server')
    return connection, jobs, duration

connection, jobs, duration = parse_json(os.path.join(os.path.curdir, 'bundle.json'))
for job_id in jobs:
    job_details = connection.scheduler.job_details(job_id)
    try:
        binary_job_file = connection.scheduler.job_output(job_id)
    except xmlrpclib.Fault:
        print 'Job output not found.'
        continue
    job_log = str(binary_job_file)
    job = Job(jobs[job_id], job_details, job_log)
    bundle_id = job.bundle_id
    if bundle_id:
        json_bundle = connection.dashboard.get(bundle_id)
        bundle = KernelCIBundle(json_bundle)
        print KernelCIResult(job, bundle).get_boot_result()