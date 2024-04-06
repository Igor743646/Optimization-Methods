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
                        required=True, help="release time")
    parser.add_argument("-dr", "--duration", default=1, type=int,
                        required=True, help="max duration")
    parser.add_argument("-due", "--due", default=1, type=int,
                        required=True, help="due")
    parser.add_argument("-we", "--weight", default=1, type=int,
                        required=True, help="max weight")
    parser.add_argument("-out", "--output-file", default="task.json", 
                        type=str, required=False, help="output file")

    return parser.parse_args()


def create_task(vertexes_count, max_duration, release, due, max_weight):

    result = {"TAU": 1, "JOBS" : {}}
    JOBS = [f"J{i}" for i in range(1, vertexes_count + 1)]

    for i, job in enumerate(JOBS):
        result["JOBS"][job] = {
            "release": release, 
            "duration": random.randint(1, max_duration + 1),
            "due": due,
            "weight": random.randint(1, max_weight + 1),
        }

    return result


def main(arguments : argparse.Namespace):
    result = {}
    vertexes_count = arguments.vertexes
    max_duration = arguments.duration
    release = arguments.release
    due = arguments.due
    max_weight = arguments.weight

    result = create_task(vertexes_count, max_duration, release, due, max_weight)

    with open(arguments.output_file, 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    args = parse_args()
    main(args)
