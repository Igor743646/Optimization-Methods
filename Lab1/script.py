import json
import argparse
from argparse import ArgumentParser
import string
import random
import networkx as nx

def parse_args() -> argparse.Namespace:
    parser = ArgumentParser()

    parser.add_argument("-mc", "--machines", default=1, type=int,
                        required=True, help="machines count")
    parser.add_argument("-vc", "--vertexes", default=1, type=int,
                        required=True, help="vertexes count")
    parser.add_argument("-rl", "--release", default=1, type=int,
                        required=True, help="release time")
    parser.add_argument("-dr", "--duration", default=1, type=int,
                        required=True, help="duration")
    parser.add_argument("-due", "--due", default=1, type=int,
                        required=True, help="due")
    parser.add_argument("-out", "--output-file", default="task.json", 
                        type=str, required=False, help="output file")

    return parser.parse_args()


def random_dag(nodes, edges):
    G = nx.DiGraph()
    for i in range(nodes):
        G.add_node(i)
    while edges > 0:
        a = random.randint(0, nodes-1)
        b = a
        while b == a:
            b = random.randint(0, nodes-1)
        if (a, b) not in G.edges():
            G.add_edge(a, b)
            if nx.is_directed_acyclic_graph(G):
                edges -= 1
            else:
                G.remove_edge(a, b)
    return G


def create_task(machines_count, vertexes_count, duration, release, due, m=5):
    result = {}
    MACHINES = [f"M{i+1}" for i in range(machines_count)]
    JOBS = list(string.ascii_uppercase[:vertexes_count])

    graph = random_dag(vertexes_count, m)
    matrix = [[1 if (i, j) in graph.edges() else 0 for j in range(vertexes_count)] for i in range(vertexes_count)]

    result["MACHINES"] = MACHINES
    result["JOBS"] = {}
    for i, job in enumerate(JOBS):
        result["JOBS"][job] = {
            "release": release, 
            "duration": duration, 
            "due": due, 
            "dependencies": [JOBS[j] for j, dep in enumerate(matrix[i]) if dep == 1]
        }

    return result


def main(arguments : argparse.Namespace):
    result = {}
    machines_count = arguments.machines 
    vertexes_count = arguments.vertexes 
    duration = arguments.duration
    release = arguments.release
    due = arguments.due

    result = create_task(machines_count, vertexes_count, duration, release, due)

    with open(arguments.output_file, 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    args = parse_args()
    main(args)
