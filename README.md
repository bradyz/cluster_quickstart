# UTCS Cluster Tutorial (for ML)

I'll cover general workflow, but another useful resource is https://www.cs.utexas.edu/~ml/faq/mastodon_readme.html

### SSH

To submit any jobs, you'll need to log into the submit nodes
Your user is your UTCS username, not your UTEID.

`ssh bzhou@jalad.cs.utexas.edu`
`ssh bzhou@darmok.cs.utexas.edu`

"The university is now requiring SSH key authentication for all SSH connections not originating from CS/CSRES networks, utexas wireless networks, or UT's VPN." Set up your ssh key here: https://www.cs.utexas.edu/ssh-keys. You will need to be on VPN to do this https://wikis.utexas.edu/pages/viewpage.action?spaceKey=networking&title=Connecting+to+the+UT+VPN+Service

Each submit node can only run 1500 jobs at a time. If you submit, your jobs will idle. When this happens, use the other submit node, I have never seen both nodes at the peak.
There is a priority queue with limited jobs, email helpreq for access.

### Cluster
There are 50 eldar nodes, each with 2 GPUs of 1080Ti or 1080.
`eldar-1` and `eldar-11` are debug nodes you can ssh onto. `ssh bzhou@eldar-1.cs.utexas.edu`

There are 5 nandor nodes, each with 8GPUs of RTX-6000(?).
`nandor-1` is a debug node you can ssh onto. `ssh jozhang@nandor-1.cs.utexas.edu`.

You cannot use multiple nodes for a single job.

### Storage

There are two main places I operate in - `$HOME`, and `/scratch/cluster/bzhou`.
If you do not have a directory in scratch space, you can try to `mkdir` in there, but otherwise email `help@cs.utexas.edu`

You are allowed a measly 20 gb in your home directory, so save this for important things.
I put my code in here, as well as experiments logs, and python installations.

Scratch is relatively flexible, I have about 400 gb, and the IT admins can give you more if you email them and cc your advisor.
I put datasets, model weights, and larger software installations in scratch.

### Python Package Manager

Anaconda, specifically Miniconda is the go-to

Follow the instructions at https://conda.io/projects/conda/en/latest/user-guide/install/linux.html - I have this installed in my home directory.
One annoying thing is that some python packages are relatively large, i.e. PyTorch being on the order of gbs, and I find myself running out of local storage all the time.

Not always does your dgx conda environment work on eldar or nandor.

### Submit a job

Condor requires a script that defines the machine requirements necessary. This is mostly annoying so there are some scripts `generate_condor.py` to get around this.

Run `python3 generate_condor.py example_project/params.py`
then `cd example_project`

and check out the files generated, `*.submit` and `*.sh`.

To submit an actual job, use `condor_submit` on a `.submit` file. Note there is nothing special about the `.submit` extension, that's just what I've named them.
To get a good grasp of what's going on, just walk through the full traceback of what happens when you run the `generate_condor.py` script.

This script uses eldar 1080s by default. To use the nandor machines, change to the following in the submit script
```
requirements = (TARGET.GPUSlot && Nandor == True)
request_GPUs = 8
```

Important: jobs are automatically pre-emptable after 24 hours.
Another job from another user may pre-empt your job.
Your job will then rerun when allocations free up.
This is debilitating if you do not have resume functionality set up.
Priority queue helps with this.


### Looking at logs

The output streams written to `example_project/logs/`, and split based on STDERR, STDOUT, etc.

## Monitoring jobs

Use `condor_q -nobatch`, I like to have this in `watch -n1.0 condor_q -nobatch` in a tmux pane at all times.

If your job is not running and you are not sure why, run `condor_q -better-analyze {job_id}` will give some hints (e.g. no machine fits your requirements).

To see who is currently using the nandor machines, run `condor_q -allusers -nobatch -run -g | grep nandor`.

## Killing jobs

Use `condor_rm id` to remove jobs via cluster id, shown in `condor_q -nobatch`.
A faster way to kill jobs is to kill all jobs, `condor_rm bzhou`.

## CARLA example

**important**: you need to edit `generate_slurm.py` to change your email, job type, etc, as well as `params.py` to change some system path information.

```bash
python3 generate_slurm.py examples/running_carla/cluster/params.py

cd examples/running_carla/cluster/slurm_scripts

sbatch n_vehicles=10.submit
```

then you can look at the running jobs using `squeue -u bzhou`.  

When your job is running/done you'll be able to check out the `examples/running_carla/cluster/logs` and see the individual STDERR, STDOUT.
