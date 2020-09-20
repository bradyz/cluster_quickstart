import argparse
import pathlib
import os


def main(project_dir, run_one, run_rest, clear_logs):
    if clear_logs:
        for f in (project_dir / 'logs').glob('*'):
            os.remove(f)

    for i, submit_file in enumerate(sorted(project_dir.glob('*.submit'))):
        run = False
        run |= i == 0 and run_one
        run |= i > 0 and run_rest

        if run:
            os.system('condor_submit %s' % submit_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', type=pathlib.Path, required=True)
    parser.add_argument('--run_one', action='store_true', default=False)
    parser.add_argument('--run_rest', action='store_true', default=False)
    parser.add_argument('--clear_logs', action='store_true', default=False)

    main(**vars(parser.parse_args()))
