import json
import argparse
from argparse import ArgumentParser
import string
import random
import networkx as nx

def parse_args() -> argparse.Namespace:
    parser = ArgumentParser()

    parser.add_argument("-vc", "--vertexes", default=1, type=int,
                        required=True, help="vertexes count")
    parser.add_argument("-rl", "--release", default=1, type=int,
                        required=True, help="max release time")
    parser.add_argument("-dr", "--duration", default=1, type=int,
                        required=True, help="max duration")
    parser.add_argument("-due", "--due", default=1, type=int,
                        required=True, help="max due")
    parser.add_argument("-out", "--output-file", default="task.json", 
                        type=str, required=False, help="output file")

    return parser.parse_args()


def create_task(vertexes_count, duration, release, due):
    assert(vertexes_count <= len(string.ascii_uppercase))
    result = {"JOBS" : {}}
    JOBS = list(string.ascii_uppercase[:vertexes_count])

    for i, job in enumerate(JOBS):
        result["JOBS"][job] = {
            "release": random.randint(0, release + 1), 
            "duration": random.randint(1, duration + 1),
            "due": random.randint(0, due + 1),
        }

    return result


def main(arguments : argparse.Namespace):
    result = {}
    vertexes_count = arguments.vertexes 
    duration = arguments.duration
    release = arguments.release
    due = arguments.due

    result = create_task(vertexes_count, duration, release, due)

    with open(arguments.output_file, 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    args = parse_args()
    main(args)
