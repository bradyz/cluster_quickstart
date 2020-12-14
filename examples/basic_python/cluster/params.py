import pathlib


HEADER = """#!/bin/bash

export SOME_VAR=123
export PYTHONPATH=$PYTHONPATH:/scratch/cluster/user_id/some_path

conda env list
"""


# Defines a grid search over these parameters.
PARAMS = {
        'arg1': [2020, 1337],
        'arg2': ['foo', 'bar']
        }


def get_job(arg1, arg2):
    """
    build your shell script here.
    """
    shell_script_str = HEADER

    # this file is /foo/bar/../basic_python/cluster/params.py
    shell_script_str += 'cd %s\n' % pathlib.Path(__file__).parent.parent

    # the script we want is /foo/bar/../basic_python/run.py
    shell_script_str += 'python3 run.py %s %s' % (arg1, arg2)

    return shell_script_str
