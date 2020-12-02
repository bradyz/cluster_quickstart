import os

from pathlib import Path


SUBMIT = """#!/bin/bash

#SBATCH --job-name {name}                    # Job name

### Logging
#SBATCH --output={log_dir}/{name}_%j.out   # Name of stdout output file (%j expands to jobId)
#SBATCH --error={log_dir}/{name}_%j.err    # Name of stderr output file (%j expands to jobId)
#SBATCH --mail-user=bzhou@cs.utexas.edu      # Email of notification
#SBATCH --mail-type=END,FAIL,REQUEUE

### Node info
###SBATCH --partition Test                   # Queue name [NOT NEEDED FOR NOW]
#SBATCH --nodes=1                            # Always set to 1 when using the cluster
#SBATCH --time 78:00:00                      # Run time (hh:mm:ss)
#SBATCH --ntasks-per-node=1                  # Number of tasks per node (Set to the number of gpus requested)
#SBATCH --gres=gpu:1                         # Number of gpus needed
#SBATCH --cpus-per-task=8                    # Number of cpus needed per task
#SBATCH --mem=48G                            # Memory requirements

./train_{name}.sh
"""


import sys
import itertools
import importlib


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()

    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


params_py = Path(sys.argv[1])
package_path = str(params_py).split('.')[0].replace('/', '.')
package = importlib.import_module(package_path)
parent = params_py.parent.resolve()

log_dir = params_py.resolve().parent / 'logs'
log_dir.mkdir(exist_ok=True)

script_dir = parent / 'slurm_scripts'
script_dir.mkdir(exist_ok=True)

for i, job_dict in enumerate(product_dict(**package.PARAMS)):
    job_name = '_'.join('%s-%s' % (k, v) for k, v in sorted(job_dict.items()))
    job = package.get_job(**job_dict)

    submit = script_dir / ('submit_%s.submit' % job_name)
    train = script_dir / ('train_%s.sh' % job_name)

    print(job_name)

    submit.write_text(SUBMIT.format(log_dir=log_dir, name=job_name))
    train.write_text(job)

    os.chmod(script_dir / ('train_%s.sh' % job_name), 509)
