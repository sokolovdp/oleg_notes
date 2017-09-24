#!/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os
from collections import Counter
from itertools import combinations
import re

import networkx as nx
import matplotlib.pyplot as plt

TAG_SYMBOL = '@'
tag_pattern = r'(?P<tag>{}\w+)'.format(TAG_SYMBOL)
tag_formula = re.compile(tag_pattern)

graph_file_name = 'full_graph.png'
subgraph_file_name = 'top_tags_graph.png'


def parse_note_line(line: "str") -> "dict":
    tags = [tag.replace(TAG_SYMBOL, '') for tag in tag_formula.findall(line)]
    note = {'tags': tags, "text": line}
    return note
    # return [tag.strip() for tag in line.strip().strip('"').split(',')]     # test CSV file


def read_note_file(file_name: "str") -> ("list", "list"):
    with open(file_name, 'r', encoding='utf-8') as notes_file:
        raw_lines = filter(lambda l: len(l) > 1, notes_file.readlines())
    notes = [parse_note_line(line.strip().lower()) for line in raw_lines]
    tags = sum([note['tags'] for note in notes], [])
    return notes, tags


def build_graph(nodes: "dict", clusters_of_edges: "list") -> "nx.Graph":
    graph = nx.Graph()
    for node, weight in nodes.items():
        graph.add_node(node, weight=weight)
    for cluster in clusters_of_edges:
        for edge in combinations(cluster, 2):
            graph.add_edge(*edge)
    return nx.freeze(graph)


def init_plot_frame():
    plt.clf()
    plt.figure(figsize=(100, 80))
    # remove all ticks (both axes), and tick labels on the Y axis
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')
    for spine in plt.gca().spines.values():  # remove the frame of the chart
        spine.set_visible(False)
    return plt


def draw_graph(graph, nodes_dict, output_file):
    plot = init_plot_frame()

    nodes_to_draw = list(nodes_dict.keys())
    nodes_sizes = [graph.node[tag]['weight'] * 500 for tag in nodes_to_draw]
    subgraph = graph.subgraph(nodes_to_draw)
    nx.draw_networkx(subgraph, pos=nx.spring_layout(graph), node_size=nodes_sizes, with_labels=True,
                     alpha=0.8, nodelist=nodes_to_draw, node_color='r')
    plot.savefig(output_file)


def tag_analysis(graph, tag):
    try:
        weight = graph.node[tag]['weight']
        neighbors = graph.neighbors(tag)
    except KeyError:
        print("error: invalid tag '{}'".format(tag))
    else:
        print("тэг '{}' имеет вес {} связан с тэгами: {}".format(tag, weight, ','.join(neighbors)))


def main(**kwargs):
    all_notes, all_tags = read_note_file(kwargs['notes_file'])
    tags_dict = Counter(all_tags)
    most_popular_tags = tags_dict.most_common(kwargs['max_top_tags'])

    print('{} заметок, {} тэгов, {} уникальных тэгов, {} самых популярных тэгов: {}'.format(
        len(all_notes),
        len(all_tags),
        len(tags_dict),
        kwargs['max_top_tags'],
        ', '.join([tag + ':' + str(weight) for tag, weight in most_popular_tags])))

    tag_graph = build_graph(tags_dict, [note['tags'] for note in all_notes])
    print("граф тэгов имеет {} вершин и {} ребер".format(tag_graph.number_of_nodes(), tag_graph.number_of_edges()))

    if kwargs['draw_graph']:
        draw_graph(tag_graph, tags_dict, graph_file_name)
        print("изображение полного графа сохранено в файле: '{}'".format(graph_file_name))

    if kwargs['draw_subgraph']:
        nodes = {tag: tags_dict[tag] for tag, _ in most_popular_tags}
        draw_graph(tag_graph, nodes, subgraph_file_name)
        print("изображение графа связи самых популярных тэгов сохранено в файле: '{}'".format(subgraph_file_name))

    for tag in kwargs['key_tags'].split(','):
        tag_analysis(tag_graph, tag)


def check_notes_file(file_name):
    if os.path.exists(file_name):
        return file_name
    raise argparse.ArgumentTypeError('invalid notes file {}'.format(file_name))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='graph analysis of text file with notes and tags')
    ap.add_argument("notes_file", type=check_notes_file, help="file with notes")
    ap.add_argument("--maxtop", dest="max_top_tags", action="store", type=int, default=10,
                    help="number of popular tags, default=10")
    ap.add_argument("--size", dest="pic_size", action="store", default='100x80', help="graph size, default=100x80")
    ap.add_argument('--graph', dest='draw_graph', action='store_true')
    ap.add_argument('--subgraph', dest='draw_subgraph', action='store_true')
    ap.add_argument('--tags', dest='key_tags', action='store', default=[])
    args = ap.parse_args(sys.argv[1:])

    main(**vars(args))
