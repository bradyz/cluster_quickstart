HEADER = """#!/bin/zsh

export SOME_VAR=123
export PYTHONPATH=$PYTHONPATH:/scratch/cluster/bzhou/some_path

cd $HOME/cluster_quickstart/example_code

conda env list
"""

PARAMS = {
        'arg1': [2020, 1337],
        'arg2': ['foo', 'bar']
        }


def get_job(arg1, arg2):
    """
    build your python command here.
    """
    return HEADER + ('python3 run.py %s %s' % (arg1, arg2)), f'exp-name-{arg1}-{arg2}'
