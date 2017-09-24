# **notes_map**
analyses of text file with notes and tags, builds graph of tags

# Usage
usage: notes_map.py [-h] [--maxtop MAX_TOP_TAGS] [--size PIC_SIZE] [--graph]
                    [--subgraph] [--tags KEY_TAGS]
                    notes_file

graph analysis of text file with notes and tags

positional arguments:
  notes_file            file with notes

optional arguments:
  -h, --help            show this help message and exit
  --maxtop MAX_TOP_TAGS
                        number of popular tags, default=10
  --size PIC_SIZE       graph size, default=100x80
  --graph
  --subgraph
  --tags KEY_TAGS

# Requirements
Python 3.6, packages: networkx, matplotlib