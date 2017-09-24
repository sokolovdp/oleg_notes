#!/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os
from collections import Counter
from itertools import combinations

import networkx as nx
import matplotlib.pyplot as plt


MAX_POPULAR_TAGS = 10


def parse_note_to_list_of_tags(line: "str") -> "list":
    return [tag.strip() for tag in line.strip().strip('"').split(',')]


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


def main(notes_file_name: "str"):
    with open(notes_file_name, 'r', encoding='utf-8') as notes_file:
        list_of_notes = list(map(parse_note_to_list_of_tags, notes_file.readlines()))

    all_tags = sum(list_of_notes, [])
    tags_dict = Counter(all_tags)
    most_popular_tags = tags_dict.most_common(MAX_POPULAR_TAGS)

    print('{} заметок, {} тэгов, {} уникальных тэгов, {} самых популярных тэгов: {}'.format(
        len(list_of_notes),
        len(all_tags),
        len(tags_dict),
        MAX_POPULAR_TAGS,
        ', '.join([tag + ':' + str(weight) for tag, weight in most_popular_tags])))

    tag_graph = build_graph(tags_dict, list_of_notes)
    print(
        "полный граф тэгов имеет {} вершин и {} ребер".format(tag_graph.number_of_nodes(), tag_graph.number_of_edges()))

    filename = 'full_graph.png'
    draw_graph(tag_graph, tags_dict, filename)
    print("изображение полного графа сохранено в файле: '{}'".format(filename))

    filename = 'popular_graph.png'
    nodes = {tag: tags_dict[tag] for tag, _ in most_popular_tags}
    draw_graph(tag_graph, nodes, filename)
    print("изображение графа связи самых популярных тэгов сохранено в файле: '{}'".format(filename))

    tag_analysis(tag_graph, 'ангина')
    tag_analysis(tag_graph, 'фото')


def check_notes_file(file_name):
    if os.path.exists(file_name):
        return file_name
    raise argparse.ArgumentTypeError('invalid notes file {}'.format(file_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='graph analysis of notes')
    parser.add_argument("notes_file", type=check_notes_file, help="file with notes")
    args = parser.parse_args(sys.argv[1:])

    main(args.notes_file)
