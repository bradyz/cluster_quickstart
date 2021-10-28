import pathlib


WORK_DIR = pathlib.Path(__file__).parent.parent
TEMPLATE = f"""#!/bin/bash

export SOME_VAR=123
export PYTHONPATH=$PYTHONPATH:/scratch/cluster/user_id/some_path

conda env list
cd {WORK_DIR}

python3 run.py """


# Defines a grid search over these parameters.
PARAMS = {
    'arg1': [2020, 1337],
    'arg2': ['foo', 'bar']
}


def get_job(arg1, arg2):
    """
    build your shell script here.
    """
    shell_script_str = TEMPLATE
    shell_script_str += f'{arg1} {arg2}'

    return shell_script_str
