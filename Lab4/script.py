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
    parser.add_argument("-ms", "--machines", default=2, type=int,
                        required=True, help="machines count")
    parser.add_argument("-rl", "--release", default=1, type=int,
                        required=True, help="release time")
    parser.add_argument("-dr", "--duration", default=1, type=int,
                        required=True, help="max duration")
    parser.add_argument("-due", "--due", default=1, type=int,
                        required=True, help="max due")
    parser.add_argument("-out", "--output-file", default="task.json", 
                        type=str, required=False, help="output file")

    return parser.parse_args()


def create_task(vertexes_count, machines_count, max_duration, release, max_due):

    MACHINES = [f"M{i}" for i in range(1, machines_count + 1)]
    result = {"MACHINES": MACHINES, "JOBS" : {}}
    JOBS = [f"J{i}" for i in range(1, vertexes_count + 1)]

    for i, job in enumerate(JOBS):
        result["JOBS"][job] = {
            "release": release, 
            "duration": [random.randint(1, max_duration + 1) for _ in MACHINES],
            "due": random.randint(0, max_due + 1)
        }

    return result


def main(arguments : argparse.Namespace):
    result = {}
    vertexes_count = arguments.vertexes
    machines_count = arguments.machines
    max_duration = arguments.duration
    release = arguments.release
    max_due = arguments.due

    result = create_task(vertexes_count, machines_count, max_duration, release, max_due)

    with open(arguments.output_file, 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    args = parse_args()
    main(args)
